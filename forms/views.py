from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from core.bitrix import check_deal, create_list, create_field, delete_list, delete_field
from core.paginator import paginator
from .forms import FormCreateForm, FormUpdateForm
from .models import Form, Field

CARDS_ON_INDEX_PAGE = 6
BASIC_FIELDS = [
    {'ФИО': 'text'},
    {'Организация': 'text'},
    {'Должность': 'text'},
    {'Почта': 'email'},
    {'Телефон': 'phone'},
    {'Комментарий': 'textarea'}
]


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
        context['basic_fields'] = BASIC_FIELDS
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
        create_list(deal_id, form.instance.deal_title)

        # Создаем базовые поля
        fields = [Field(label=label, field_type=field_type, form_id=form_id, is_active=False) for
                  field_data in BASIC_FIELDS for label, field_type in field_data.items()]
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
                if field_data[1].isdigit():
                    field_num = int(field_data[1])
                    label = self.request.POST.get(f'custom_field-{field_num}-label')
                    field_type = self.request.POST.get(f'custom-{field_num}-field_type')
                    field = Field.objects.create(
                        form_id=form_id,
                        label=label,
                        field_type=field_type,
                        is_active=True,
                    )
                    # Сохраняем поле в Битрикс
                    result = create_field(deal_id, field.label)
                    field.bitrix_id = result
                    # Сохраняем поле в БД
                    field.save()

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
        context['form_link'] = self.object.form_link
        context['deal_id'] = self.object.deal_id
        context['fields'] = self.object.fields.all().order_by('id')
        return context

    def form_valid(self, form):
        """Переопределяем метод формы для сохранения изменений связанных полей поля формы."""

        # Получаем список всех полей формы
        fields = self.object.fields.all()

        # Проходимся по каждому полю и проверяем его статус в форме
        for field in fields:
            field_id = 'field-{}-{}'.format(field.field_type, field.id)
            field.is_active = field_id in self.request.POST
            # Изменяем поле в Битрикс
            if field.is_active:
                result = create_field(self.object.deal_id, field.label)
                if result:
                    field.bitrix_id = result
            else:
                delete_field(self.object.deal_id, field.bitrix_id)
            field.save()

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
