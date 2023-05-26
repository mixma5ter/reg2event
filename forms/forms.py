from django import forms

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
        # Проверяем, есть ли запись в БД с таким deal_id
        if Form.objects.filter(deal_id=deal_id).exists():
            raise forms.ValidationError('Форма с ID мероприятия {} уже существует!'.format(deal_id))

        # Проверяем, есть ли сделка в Битрикс с таким deal_id
        # если есть, получаем название мероприятия и дату проведения TODO

        # Проверяем дату проведения мероприятия TODO

        return deal_id
