from django import forms
from django.forms import CheckboxInput, EmailInput, Select, Textarea, TextInput
from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from forms.models import Form, FieldChoice


class SeparatorWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f"<hr><strong>{name}</strong>")

    def value_from_datadict(self, data, files, name):
        return None

    def get_class_name(self):
        return self.__class__.__name__


class CustomTextarea(forms.CharField):
    widget = Textarea

    def validate(self, value):
        super().validate(value)
        text_length = len(value.strip())
        if self.max_length is not None and text_length > self.max_length:
            raise forms.ValidationError(
                f"Убедитесь, что это текст содержит не более {self.max_length} символов "
                f"(сейчас {text_length})."
            )


class RegForm(forms.Form):
    def __init__(self, *args, deal_id, **kwargs):
        super().__init__(*args, **kwargs)
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        active_fields = reg_form.fields.filter(is_active=True).order_by('order_id')
        for field in active_fields:
            if field.field_type == 'text':
                self.fields[field.label] = forms.CharField(
                    max_length=100,
                    widget=TextInput(attrs={'class': 'form-control'}))
            elif field.field_type == 'textarea':
                self.fields[field.label] = CustomTextarea(
                    max_length=955,
                    required=False,
                    widget=Textarea(attrs={'class': 'form-control'}))
            elif field.field_type == 'number':
                self.fields[field.label] = forms.IntegerField(
                    widget=TextInput(attrs={'class': 'form-control'}))
            elif field.field_type == 'email':
                self.fields[field.label] = forms.EmailField(
                    max_length=100,
                    widget=EmailInput(attrs={'class': 'form-control'}))
            elif field.field_type == 'phone':
                self.fields[field.label] = forms.CharField(
                    max_length=14,
                    widget=TextInput(attrs={'class': 'form-control'}))
            elif field.field_type == 'checkbox':
                self.fields[field.label] = forms.BooleanField(
                    required=False,
                    widget=CheckboxInput(attrs={'class': 'form-check-input'}))
            elif field.field_type == 'select':
                choices = FieldChoice.objects.filter(field=field).order_by('id')
                # Добавляем пустой вариант в качестве параметра по умолчанию или заполнителя
                choice_list = [('', '---')]
                # Добавляем оставшиеся варианты из базы данных
                choice_list += [(choice.choice_text, choice.choice_text) for choice in choices]
                self.fields[field.label] = forms.ChoiceField(
                    choices=choice_list,
                    initial='',  # Устанавливаем начальное значение в пустую строку
                    widget=Select(attrs={'class': 'form-control custom-select'}))
            elif field.field_type == 'separator':
                self.fields[field.label] = forms.CharField(
                    required=False,
                    widget=SeparatorWidget(attrs={'class': 'form-control', 'readonly': True}))
