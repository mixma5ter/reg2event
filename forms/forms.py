from django import forms
from django.forms import DateTimeInput
from django.http import JsonResponse

from core.bitrix import get_deal
from .models import Form

MAX_VALUE = 8  # максимальное длина числа в ID мероприятия


def check_deal(deal_id):
    """Валидация сделки в Битрикс."""

    # Проверяем, что длина числа не превышает 10 символов
    if len(str(deal_id)) > MAX_VALUE:
        return {'value': False, 'message': 'Слишком большое значение ID мероприятия!'}

    # Проверяем, есть ли запись в БД с таким deal_id
    if Form.objects.filter(deal_id=deal_id).exists():
        return {'value': False, 'message': f'Форма с ID мероприятия {deal_id} уже существует!'}

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
        return {'value': False, 'message': f'Сделка с ID {deal_id} уже закрыта!'}

    if response.status_code != 200:
        return {'value': False, 'message': 'Ошибка запроса к Битрикс! Проверьте ID мероприятия!'}

    # При успешной валидации, выводим название сделки
    message = data['result']['TITLE']
    return {'value': True, 'message': message}


def check_deal_ajax(request, deal_id):
    """Функция проверки deal_id с помощью Ajax запроса."""

    result = check_deal(deal_id)
    return JsonResponse({'value': result.get('value'), 'message': result.get('message')})


class BaseFormMixin(forms.ModelForm):
    """Базовый класс формы."""

    class Meta:
        model = Form
        fields = ('title', 'stream_link', 'end_date',)
        help_texts = {
            'title': 'Введите название мероприятия',
            'stream_link': 'Добавьте ссылку на трансляцию',
            'end_date': 'Укажите дату окончания регистрации',
        }
        labels = {
            'title': 'Название формы',
            'stream_link': 'Ссылка на трансляцию',
            'end_date': 'Дата окончания регистрации',
        }

    stream_link = forms.URLField(
        required=False,
        label='Ссылка на трансляцию',
        help_text='Введите ссылку на трансляцию',
    )

    end_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        label='Дата окончания регистрации',
    )

    def clean_deal_id(self):
        deal_id = self.cleaned_data['deal_id']
        result = check_deal(deal_id)
        if not result.get('value'):
            raise forms.ValidationError(result.get('message'))
        return deal_id


class FormCreateForm(BaseFormMixin, forms.ModelForm):
    """Форма добавляет новую форму в БД."""

    class Meta(BaseFormMixin.Meta):
        fields = ('deal_id',) + BaseFormMixin.Meta.fields
        help_texts = {
            'deal_id': 'Введите ID мероприятия',
        }
        labels = {
            'deal_id': 'ID мероприятия',
        }


class FormUpdateForm(BaseFormMixin, forms.ModelForm):
    """Форма изменяет форму в БД."""

    class Meta(BaseFormMixin.Meta):
        pass  # используем все поля и подписи из BaseFormMixin.Meta
