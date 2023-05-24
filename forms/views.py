from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from core.paginator import paginator
from .forms import FormCreateForm
from .models import Form, Field

CARDS_ON_INDEX_PAGE = 6


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
    template_name = 'forms/forms_list.html'
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
    success_url = reverse_lazy('forms:form_create')
    title = 'Новая форма регистрации'

    def form_valid(self, form):
        # Проверяем, есть ли сделка в Биртрикс с таким deal_id
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

        # Получаем поля формы Field из POST-запроса и сохраняем их в БД
        fields = []
        for key, value in self.request.POST.items():
            # Получаем базовые поля
            if key.startswith('field-'):
                if value == 'on':
                    field_data = key.split('-')
                    field = Field(
                        label=field_data[2],
                        field_type=field_data[1],
                        form=form.instance,
                    )
                    field.save()
            # Получаем кастомные поля
            elif key.startswith('custom-'):
                field_data = key.split('-')
                index = int(field_data[1])
                field_key = field_data[2]
                if index >= len(fields):
                    fields.append({})
                fields[index][field_key] = value
        # Сохраняем объекты Field в БД
        for field_data in fields:
            field = Field(
                label=field_data['label'],
                field_type=field_data['field_type'],
                form=form.instance,
            )
            field.save()

        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
