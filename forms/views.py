from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from core.paginator import paginator
from .forms import FormCreateForm
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

    def get_queryset(self):
        cards = Form.objects.all().order_by('-pub_date')[:CARDS_ON_INDEX_PAGE]
        return cards

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['cards'] = self.get_queryset()
        return context


class FormsListView(LoginRequiredMixin, ListView):
    """Страница со списком форм регистрации."""

    model = Form
    template_name = 'forms/form_list.html'
    context_object_name = 'forms'
    title = 'Формы регистраций'

    def get_queryset(self):
        return Form.objects.all().order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
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

    def form_valid(self, form):
        # Проверяем, есть ли сделка в Битрикс с таким deal_id
        # если есть, получаем название мероприятия и дату проведения TODO

        # Проверяем дату проведения мероприятия TODO

        # Проверяем, есть ли запись в БД с таким deal_id
        deal_id = form.cleaned_data['deal_id']
        if Form.objects.filter(deal_id=deal_id).exists():
            messages.warning(self.request, 'Форма с данным ID мероприятия уже существует!')
            return super().form_invalid(form)
        form.instance.author = self.request.user
        # Сохраняем объект Form в БД
        form.save()
        # Получаем id созданной записи
        form_id = form.instance.id

        # Создаем базовые поля
        fields = []
        for field_data in BASIC_FIELDS:
            label, field_type = list(field_data.items())[0]
            field = Field(label=label, field_type=field_type, form_id=form_id, is_active=False)
            fields.append(field)
        Field.objects.bulk_create(fields)

        # Получаем поля формы Field из POST-запроса и сохраняем их в БД
        for key, value in self.request.POST.items():
            # Изменяем базовые поля
            if key.startswith('field-'):
                field_data = key.split('-')
                field = Field.objects.filter(form_id=form_id, label=field_data[2]).first()
                if field:
                    field.is_active = True if value == 'on' else False
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
                    field.save()

        success_url = reverse_lazy('forms:form_detail', args=[form_id])
        return redirect(success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['basic_fields'] = BASIC_FIELDS
        return context


class FormDetailView(LoginRequiredMixin, UpdateView):
    """Контроллер для просмотра и редактирования формы."""

    model = Form
    form_class = FormCreateForm
    template_name = 'forms/form_detail.html'
    context_object_name = 'form'
    success_url = reverse_lazy('forms:forms_list')
    title = 'Редактирование формы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем id формы в контекст шаблона
        context['form_id'] = self.object.id
        context['title'] = self.title
        context['fields'] = self.object.fields.all().order_by('id')
        return context

    def form_valid(self, form):
        """Переопределяем метод формы для сохранения изменений связанных полей поля формы."""
        self.object = form.save(commit=False)
        self.object.save()

        fields_data = []
        for key, value in self.request.POST.items():
            if key.startswith('field-'):
                field_id = key.split('-')[1]
                field_data = {'id': field_id}
                if value == 'on':
                    field_data['value'] = True
                else:
                    field_data['value'] = value
                fields_data.append(field_data)

        for field_data in fields_data:
            field_id = field_data.pop('id')
            Field.objects.filter(id=field_id).update(**field_data)

        return super().form_valid(form)
