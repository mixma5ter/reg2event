from django import forms
from django.forms import EmailInput, TextInput
from django.shortcuts import get_object_or_404

from forms.models import Form


class RegForm(forms.Form):
    def __init__(self, *args, **kwargs):
        deal_id = kwargs.pop('deal_id')
        super().__init__(*args, **kwargs)
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        active_fields = reg_form.fields.filter(is_active=True).order_by('pk')
        for field in active_fields:
            if field.field_type == 'text':
                self.fields[field.label] = forms.CharField(max_length=100, widget=TextInput(
                    attrs={'class': 'form-control'}))
            elif field.field_type == 'textarea':
                self.fields[field.label] = forms.CharField(max_length=255, widget=TextInput(
                    attrs={'class': 'form-control'}))
            elif field.field_type == 'number':
                self.fields[field.label] = forms.IntegerField(
                    widget=TextInput(attrs={'class': 'form-control'}))
            elif field.field_type == 'email':
                self.fields[field.label] = forms.EmailField(max_length=100, widget=EmailInput(
                    attrs={'class': 'form-control'}))
            elif field.field_type == 'phone':
                self.fields[field.label] = forms.CharField(max_length=12, widget=TextInput(
                    attrs={'class': 'form-control'}))
            elif field.field_type == 'checkbox':
                self.fields[field.label] = forms.BooleanField(
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
