from django import forms
from django.http import JsonResponse

from core.bitrix import get_deal
from .models import Form

MAX_VALUE = 8  # максимальное длина числа в ID мероприятия


def check_deal(deal_id):
    """Валидация сделки в Битрикс."""

    # Проверяем, что длина числа не превышает 10 символов
    if len(str(deal_id)) > MAX_VALUE:
        return {'value': False, 'message': 'Слишком большое значение ID мероприятия!'}

    # Проверяем, есть ли сделка в Битрикс с таким deal_id
    response = get_deal(deal_id)
    data = response.json()
    if data.get('error'):
        return {'value': False, 'message': 'Ошибка получения данных из Битрикс!'}
    if not data.get('result'):
        return {'value': False, 'message': 'Нет сделки с таким ID!'}

    # Проверяем статус сделки
    is_closed_str = data['result']['CLOSED']
    if is_closed_str == 'Y':
        return {'value': False, 'message': 'Сделка с ID {} уже закрыта!'.format(deal_id)}

    if response.status_code != 200:
        return {'value': False, 'message': 'Ошибка запроса к Битрикс! Проверьте ID мероприятия!'}

    # При успешной валидации, выводим название сделки
    return {'value': True, 'message': data['result']['TITLE']}


def check_deal_ajax(request, deal_id):
    """Функция проверки deal_id с помощью Ajax запроса."""

    result = check_deal(deal_id)
    return JsonResponse({'value': result.get('value'), 'message': result.get('message')})


class FormCreateForm(forms.ModelForm):
    """Форма добавляет новую форму в БД."""

    class Meta:
        model = Form
        fields = ('deal_id', 'title', 'stream_link',)
        help_texts = {
            'deal_id': 'Введите ID мероприятия',
            'title': 'Введите название мероприятия',
            'stream_link': 'Добавьте ссылку на трансляцию',
        }
        labels = {
            'deal_id': 'ID мероприятия',
            'title': 'Название формы',
            'stream_link': 'Ссылка на трансляцию',
        }

    def clean_deal_id(self):
        deal_id = self.cleaned_data['deal_id']
        result = check_deal(deal_id)
        if not result.get('value'):
            raise forms.ValidationError(result.get('message'))
        return deal_id


class FormUpdateForm(forms.ModelForm):
    """Форма изменяет форму в БД."""

    class Meta:
        model = Form
        fields = ('title', 'stream_link',)
        help_texts = {
            'title': 'Введите название мероприятия',
            'stream_link': 'Добавьте ссылку на трансляцию',
        }
        labels = {
            'title': 'Название формы',
            'stream_link': 'Ссылка на трансляцию',
        }
