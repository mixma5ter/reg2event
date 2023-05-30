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

        # Получаем модель формы по ID
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        # Получаем поля формы связанные с формой
        reg_fields = reg_form.fields.all().filter(is_active=True).order_by('pk')
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
        fields = {}
        for field in reg_fields:
            if field.label in data:
                fields[field.label] = data[field.label]

        # Отправляем запрос на создание сделки в Битрикс24 по вебхуку
        url = '{}crm.deal.add.json'.format(WEB_HOOK)
        headers = {'Content-Type': 'application/json'}
        params = {
            'fields': {
                'TITLE': 'Тестовая сделка',  # название новой сделки
                'STAGE_ID': 'C10:NEW',  # этап сделки
                'CATEGORY_ID': 10,  # регистрация
                'ASSOCIATED_DEAL_ID': deal_id,  # ID связанной сделки
            },
            'params': {'REGISTER_SONET_EVENT': 'Y'},
        }
        response = requests.get(url, headers=headers, json=params)

        # Обрабатываем ответ от Битрикс24
        if response.ok:
            message = 'Сделка успешно создана!'
            messages.success(self.request, message)
        else:
            message = 'Ошибка при создании сделки!'
            messages.warning(self.request, message)

        context = {
            'title': message,
        }
        return render(request, template_name, context)
