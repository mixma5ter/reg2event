import requests
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views import View

from config.settings import WEB_HOOK
from forms.models import Form


class RegView(View):
    """Страница регистрации пользователей на мероприятие."""

    def get(self, request, deal_id):
        """Получение формы из БД."""

        template_name = 'reg/reg_form.html'

        # Получаем модель формы по deal_id
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        # Получаем поля формы связанные с формой и со значением is_active=True
        reg_fields = reg_form.fields.filter(is_active=True).order_by('pk')
        context = {
            'reg_form': reg_form,
            'reg_fields': reg_fields,
        }
        return render(request, template_name, context)

    def post(self, request, deal_id):
        """Отправка формы в Битрикс."""

        template_name = 'reg/reg_done.html'

        # Получаем модель формы по ID
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        # Получаем поля формы связанные с формой
        reg_fields = reg_form.fields.all().filter(is_active=True).order_by('pk')

        # Получаем данные из POST-запроса
        data = request.POST.dict()

        # Формируем данные для создания сделки в Битрикс24
        fields = {field.label: data.get(field.label, '') for field in reg_fields}

        # Отправляем запрос на создание сделки в Битрикс24 по вебхуку
        url = '{}crm.deal.add.json'.format(WEB_HOOK)
        params = {
            'fields': {
                'TITLE': reg_form.title,  # название новой сделки
                'STAGE_ID': 'C10:NEW',  # этап сделки
                'CONTACT_ID': 262,
                'CATEGORY_ID': 10,  # регистрация
                'COMMENTS': 'Комментарий: тестовая сделка для проверки работы вэбхука',
                'OPENED': 'Y',
                'CLOSED': 'Y',
                'SOURCE_ID': 'WEBFORM',  # Источник
                'SOURCE_DESCRIPTION': 'Автоматически созданная сделка',
                'ASSIGNED_BY_ID': '12',
                'CREATED_BY_ID': '12',
                'MOVED_BY_ID': '12',
                'LAST_ACTIVITY_BY': '12',

                'UF_CRM_1666041653': reg_form.title,  # Р: Мероприятие
            },
            'params': {'REGISTER_SONET_EVENT': 'Y'},
        }
        # Добавление полей из формы в параметры запроса
        params['fields'].update(fields)
        response = requests.post(url, json=params)

        # Обрабатываем ответ от Битрикс24
        if response.ok:
            message = 'Сделка успешно создана!'
            messages.success(request, message)
        else:
            message = 'Ошибка при создании сделки!'
            messages.warning(request, message)

        context = {
            'title': message,
        }
        return render(request, template_name, context)
