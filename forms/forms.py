from django import forms

from .models import Form


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
