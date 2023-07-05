from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from core.bitrix import create_element
from forms.models import Form
from reg.forms import RegForm


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class RegView(View):
    """Страница регистрации пользователей на мероприятие."""

    model = Form
    form_class = RegForm
    template_name = 'reg/reg_form.html'
    context_object_name = 'reg'

    def get_form_obj(self, deal_id):
        return get_object_or_404(Form, deal_id=deal_id)

    def check_end_date(self, form_obj):
        """Проверка даты окончания регистрации."""
        if form_obj.end_date < timezone.now():
            return True
        return False

    def get(self, request, deal_id):
        # Проверка даты окончания регистрации
        form_obj = self.get_form_obj(deal_id)
        if self.check_end_date(form_obj):
            return redirect('reg:reg_info', deal_id=deal_id, slug='closed')

        title = form_obj.title
        reg_form = self.form_class(deal_id=deal_id)
        context = {
            'title': title,
            'form': reg_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, deal_id):
        # Проверка даты окончания регистрации
        form_obj = self.get_form_obj(deal_id)
        if self.check_end_date(form_obj):
            return redirect('reg:reg_info', deal_id=deal_id, slug='closed')

        reg_form = self.form_class(request.POST, deal_id=deal_id)
        if reg_form.is_valid():
            form = get_object_or_404(Form, deal_id=deal_id)

            fields = {'NAME': form.title}

            for field in form.fields.all():
                key = field.bitrix_id
                value = request.POST.get(field.label)
                # Записываем значение в поле checkbox
                if field.field_type == 'checkbox':
                    if value:
                        value = 'да'
                    else:
                        value = 'нет'
                if value:
                    fields[key] = value

            create_element(deal_id, fields)
            return redirect('reg:reg_info', deal_id=deal_id, slug='success')

        title = self.get_form_obj(deal_id).title
        context = {
            'title': title,
            'form': reg_form,
            'errors': reg_form.errors.items()
        }
        return render(request, self.template_name, context)


@method_decorator(require_http_methods(['GET']), name='dispatch')
class RegInfoView(View):
    """Страница информации о регистрации."""

    template_name = 'reg/reg_info.html'

    def get(self, request, deal_id, slug):
        form = get_object_or_404(Form, deal_id=deal_id)
        stream_link = form.stream_link if slug != 'error' else None
        new_reg = True if slug != 'closed' else False

        context = {
            'deal_id': deal_id,
            'title': {
                'success': 'Регистрация прошла успешно',
                'closed': 'Регистрация закрыта',
                'error': 'Возникла ошибка при регистрации'
            }.get(slug, 'Регистрация прошла успешно'),
            'stream_link': stream_link,
            'new_reg': new_reg,
        }
        return render(request, self.template_name, context)
