from django import forms
from django.forms import EmailInput, Textarea, TextInput
from django.shortcuts import get_object_or_404

from forms.models import Form


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
        active_fields = reg_form.fields.filter(is_active=True).order_by('pk')
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
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
