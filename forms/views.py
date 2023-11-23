from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from config.settings import DOMAIN_NAME, LINK_FIELD
from core.bitrix import (check_deal, create_list, create_field,
                         delete_list, delete_field, update_deal_field,
                         LIST_TEMPLATE)
from core.paginator import paginator
from .forms import FormCreateForm, FormUpdateForm
from .models import BasicField, Form, Field, FieldChoice

CARDS_ON_INDEX_PAGE = 6
ORDER_ID_MULTIPLE = 10


class IndexView(LoginRequiredMixin, ListView):
    """Главная страница."""

    model = Form
    template_name = 'forms/index.html'
    context_object_name = 'forms'
    title = 'Формы регистраций'
    paginate_by = CARDS_ON_INDEX_PAGE

    def get_queryset(self):
        return super().get_queryset().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class FormsListView(LoginRequiredMixin, ListView):
    """Страница со списком форм регистрации."""

    model = Form
    template_name = 'forms/form_list.html'
    context_object_name = 'forms'
    title = 'Формы регистраций'

    def get_queryset(self):
        return super().get_queryset().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['page_obj'], context['page_numbers'] = paginator(self.request, self.get_queryset())
        return context


class FormCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для добавления новой формы."""

    model = Form
    form_class = FormCreateForm
    template_name = 'forms/form_create.html'
    context_object_name = 'form'
    title = 'Новая форма регистрации'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['basic_fields'] = BasicField.objects.filter(visible=True).order_by('order_id')
        return context

    def form_valid(self, form):
        deal_id = form.cleaned_data['deal_id']
        # Проверяем, есть ли запись в БД с таким deal_id
        if Form.objects.filter(deal_id=deal_id).exists():
            message_template = 'Форма с ID мероприятия {} уже существует!'
            messages.warning(self.request, message_template.format(deal_id))
            return super().form_invalid(form)

        # Конструктор ссылки на страницу регистрации
        form.instance.form_link = reverse('reg:reg_form', args=[form.instance.deal_id])

        # Добавляем автора
        form.instance.author = self.request.user
        # Добавляем название сделки
        form.instance.deal_title = check_deal(deal_id).get('result')['TITLE']
        # Сохраняем объект Form в БД
        form.save()
        # Получаем id созданной записи
        form_id = form.instance.id

        # Создаем список в Битрикс
        list_id = create_list(deal_id, form.instance.deal_title)

        # Создаем базовые поля
        basic_fields = BasicField.objects.filter(visible=True).order_by('order_id')
        fields = [Field(label=item.label,
                        field_type=item.field_type,
                        order_id=item.order_id,
                        form_id=form_id,
                        is_active=False) for item in basic_fields]

        max_order_id = max([field.order_id for field in basic_fields])
        order_id_counter = max_order_id + ORDER_ID_MULTIPLE

        # Создаем дополнительные поля для даты и времени
        fields.extend([Field(label='Дата',
                             field_type='date',
                             order_id=order_id_counter,
                             form_id=form_id,
                             is_active=True,
                             bitrix_id=create_field(deal_id, 'Дата')),
                       Field(label='Время',
                             field_type='time',
                             order_id=order_id_counter + ORDER_ID_MULTIPLE,
                             form_id=form_id,
                             is_active=True,
                             bitrix_id=create_field(deal_id, 'Время'))
                       ])

        order_id_counter += ORDER_ID_MULTIPLE

        Field.objects.bulk_create(fields)

        # Получаем поля формы Field из POST-запроса и сохраняем их в БД
        for key, value in self.request.POST.items():
            # Получаем базовые поля
            if key.startswith('field-'):
                field_data = key.split('-')
                field = Field.objects.filter(form_id=form_id, label=field_data[2]).first()
                if field:
                    field.is_active = value == 'on'
                    # Сохраняем поле в Битрикс
                    result = create_field(deal_id, field.label)
                    field.bitrix_id = result
                    # Сохраняем поле в БД
                    field.save()

            # Получаем кастомные поля
            elif key.startswith('custom_field-'):
                field_data = key.split('-')
                order_id_counter += ORDER_ID_MULTIPLE
                if field_data[1].isdigit():
                    field_num = int(field_data[1])
                    label = self.request.POST.get(f'custom_field-{field_num}-label')
                    field_type = self.request.POST.get(f'custom-{field_num}-field_type')
                    field = Field.objects.create(
                        form_id=form_id,
                        label=label,
                        order_id=order_id_counter,
                        field_type=field_type,
                        is_active=True,
                    )
                    # Сохраняем поле в Битрикс
                    result = create_field(deal_id, field.label)
                    field.bitrix_id = result
                    # Сохраняем поле в БД
                    field.save()

                    # Сохраняем элементы выбора в модель FieldChoice
                    if field_type == 'select':
                        choices = self.request.POST.getlist(f'custom-{field_num}-list_item')
                        field_choices = [FieldChoice(field=field,
                                                     choice_text=choice) for choice in choices]
                        FieldChoice.objects.bulk_create(field_choices)

        # Обновление ссылки на список в сделке Битрикс24
        update_deal_field(deal_id, LINK_FIELD, LIST_TEMPLATE.format(list_id))

        messages.success(self.request, 'Форма успешно создана!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forms:form_update', args=[self.object.id])


class FormUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для просмотра, редактирования и удаления формы."""

    model = Form
    form_class = FormUpdateForm
    template_name = 'forms/form_update.html'
    context_object_name = 'form'
    title = 'Форма регистрации'
    success_url = reverse_lazy('forms:form_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['domain_name'] = DOMAIN_NAME
        context['form_link'] = self.object.form_link
        context['deal_id'] = self.object.deal_id
        context['fields'] = self.object.fields.all().order_by('order_id')
        return context

    def process_fields(self, fields):
        # Обработка базовых полей
        for field in fields:
            field_id = 'field-{}-{}'.format(field.field_type, field.id)
            if field.field_type in ['time', 'date']:
                continue
            field.is_active = field_id in self.request.POST
            if field.is_active:
                result = create_field(self.object.deal_id, field.label)
                if result:
                    field.bitrix_id = result
            else:
                delete_field(self.object.deal_id, field.bitrix_id)
            field.save()

    def process_custom_fields(self, deal_id, form_id, order_id_counter):
        # Обработка кастомных полей
        for key, value in self.request.POST.items():
            if key.startswith('custom_field-'):
                field_data = key.split('-')
                if field_data[1].isdigit():
                    field_num = int(field_data[1])
                    label = self.request.POST.get(f'custom_field-{field_num}-label')
                    field_type = self.request.POST.get(f'custom-{field_num}-field_type')
                    field = Field.objects.create(
                        form_id=form_id,
                        label=label,
                        order_id=order_id_counter,
                        field_type=field_type,
                        is_active=True,
                    )
                    order_id_counter += ORDER_ID_MULTIPLE
                    result = create_field(deal_id, field.label)
                    field.bitrix_id = result
                    field.save()
                    if field_type == 'select':
                        choices = self.request.POST.getlist(f'custom-{field_num}-list_item')
                        field_choices = [FieldChoice(field=field,
                                                     choice_text=choice) for choice in choices]
                        FieldChoice.objects.bulk_create(field_choices)

    def form_valid(self, form):
        """Переопределяем метод формы для сохранения изменений связанных полей поля формы."""

        deal_id = self.object.deal_id
        form_id = form.instance.id
        # Получаем список всех полей формы
        fields = self.object.fields.all()
        # Проходимся по каждому полю и проверяем его статус в форме
        self.process_fields(fields)
        # Получаем максимальное значение order_id
        max_order_id = fields.order_by('-order_id').first().order_id if fields else 0
        order_id_counter = max_order_id + ORDER_ID_MULTIPLE
        # Получаем поля формы Field из POST-запроса и сохраняем их в БД
        self.process_custom_fields(deal_id, form_id, order_id_counter)

        messages.success(self.request, 'Форма успешно обновлена!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            form = self.get_object()
            form.delete()
            # Удаляем список в Битрикс
            delete_list(form.deal_id)
            messages.success(self.request, 'Форма успешно удалена!')
            return redirect('forms:form_list')
        else:
            return super().post(request, *args, **kwargs)
