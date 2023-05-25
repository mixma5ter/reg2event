from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
    paginate_by = CARDS_ON_INDEX_PAGE

    def get_queryset(self):
        return Form.objects.order_by('-pub_date')  # [:CARDS_ON_INDEX_PAGE]

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
        return Form.objects.order_by('-pub_date')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['basic_fields'] = BASIC_FIELDS
        return context

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

        form.instance.link = 'http://example.com/api/{}'.format(deal_id)

        # Сохраняем объект Form в БД
        form.save()
        # Получаем id созданной записи
        form_id = form.instance.id

        # Создаем базовые поля
        fields = [Field(label=label, field_type=field_type, form_id=form_id, is_active=False) for
                  field_data in BASIC_FIELDS for label, field_type in field_data.items()]
        Field.objects.bulk_create(fields)

        # Получаем поля формы Field из POST-запроса и сохраняем их в БД
        for key, value in self.request.POST.items():
            # Изменяем базовые поля
            if key.startswith('field-'):
                field_data = key.split('-')
                field = Field.objects.filter(form_id=form_id, label=field_data[2]).first()
                if field:
                    field.is_active = value == 'on'
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

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forms:form_detail', args=[self.object.id])


class FormUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер для просмотра и редактирования формы."""

    model = Form
    form_class = FormCreateForm
    template_name = 'forms/form_update.html'
    context_object_name = 'form'
    title = 'Форма регистрации'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем id формы в контекст шаблона
        context['title'] = self.title
        context['link'] = self.object.link
        context['fields'] = self.object.fields.all().order_by('id')
        return context

    def form_valid(self, form):
        """Переопределяем метод формы для сохранения изменений связанных полей поля формы."""

        self.object = form.save(commit=False)

        deal_id = form.cleaned_data['deal_id']
        self.object.link = 'http://example.com/api/{}'.format(deal_id)

        # Получаем список всех полей формы
        fields = self.object.fields.all()

        # Проходимся по каждому полю и проверяем его статус в форме
        for field in fields:
            field_id = 'field-{}-{}'.format(field.field_type, field.id)
            field.is_active = field_id in self.request.POST
            field.save()

        self.object.save()
        messages.success(self.request, 'Форма успешно обновлена!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forms:form_list')
