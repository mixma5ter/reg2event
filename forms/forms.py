import requests
from django import forms

from config.settings import WEB_HOOK
from .models import Form

MAX_VALUE = 8  # максимальное длина числа в ID мероприятия


class FormCreateForm(forms.ModelForm):
    """Форма добавляет новую форму в БД."""

    class Meta:
        model = Form
        fields = ('deal_id', 'title',)
        help_texts = {
            'deal_id': 'Введите ID мероприятия',
            'title': 'Введите название мероприятия',
        }
        labels = {
            'deal_id': 'ID мероприятия',
            'title': 'Название формы',
        }

    def clean_deal_id(self):
        deal_id = self.cleaned_data['deal_id']
        # Проверяем, что длина числа не превышает 10 символов
        if len(str(deal_id)) > MAX_VALUE:
            raise forms.ValidationError('Слишком большое значение ID мероприятия!')

        # Проверяем, есть ли сделка в Битрикс с таким deal_id
        # если есть, получаем название мероприятия и дату проведения
        url = '{}crm.deal.get'.format(WEB_HOOK)
        payload = {'id': deal_id}
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            raise forms.ValidationError('Ошибка запроса к Битрикс! Проверьте ID мероприятия!')

        data = response.json()
        if data.get('error'):
            raise forms.ValidationError('Ошибка получения данных из Битрикс!')

        if not data.get('result'):
            raise forms.ValidationError('Нет сделки с таким ID!')

        # Проверяем статус сделки
        is_closed_str = data['result']['CLOSED']
        if is_closed_str == 'Y':
            raise forms.ValidationError('Сделка с ID {} уже закрыта!'.format(deal_id))

        return deal_id


class FormUpdateForm(forms.ModelForm):
    """Форма изменяет форму в БД."""

    class Meta:
        model = Form
        fields = ('title',)
        help_texts = {
            'title': 'Введите название мероприятия',
        }
        labels = {
            'title': 'Название формы',
        }
