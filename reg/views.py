from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from core.bitrix import create_element, get_deal
from forms.models import Form
from reg.forms import RegForm


class RegView(View):
    """Страница регистрации пользователей на мероприятие."""

    model = Form
    form_class = RegForm
    template_name = 'reg/reg_form.html'
    context_object_name = 'reg'
    title = 'Регистрация'

    def get(self, request, deal_id):
        reg_form = self.form_class(deal_id=deal_id)
        context = {
            'title': self.title,
            'form': reg_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, deal_id):
        # Проверяем, есть ли сделка в Битрикс с таким deal_id
        response = get_deal(deal_id)
        data = response.json()
        # Если есть ошибки при запросе или сделка уже закрыта
        # отправляем пользователя на страницу неудачной регистрации
        if (response.status_code != 200 or not data.get('result') or
                data.get('error') or data['result']['CLOSED'] == 'Y'):
            return redirect('reg:reg_error', deal_id=deal_id)

        reg_form = self.form_class(request.POST, deal_id=deal_id)
        if reg_form.is_valid():
            form = get_object_or_404(Form, deal_id=deal_id)

            fields = {'NAME': 'Регистрация'}
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

            # Создание нового элемента в Битрикс
            session = request.session.session_key

            response = create_element(deal_id, session, fields)
            if response.ok:
                return redirect('reg:reg_done', deal_id=deal_id)
            else:
                return redirect('reg:reg_error', deal_id=deal_id)

        else:
            context = {
                'title': self.title,
                'form': reg_form,
                'errors': reg_form.errors.items()
            }
            return render(request, self.template_name, context)


class RegDoneView(View):
    """Страница успешной регистрации."""

    model = Form
    template_name = 'reg/reg_done.html'
    context_object_name = 'reg'
    title = 'Регистрация успешно завершена'

    def get(self, request, deal_id):
        stream_link = get_object_or_404(Form, deal_id=deal_id).stream_link
        context = {
            'deal_id': deal_id,
            'title': self.title,
            'stream_link': stream_link,
        }
        return render(request, self.template_name, context)


class RegErrorView(View):
    """Страница неудачной регистрации."""

    model = Form
    template_name = 'reg/reg_error.html'
    context_object_name = 'reg'
    title = 'Возникла ошибка при регистрации'

    def get(self, request, deal_id):
        context = {
            'deal_id': deal_id,
            'title': self.title,
        }
        return render(request, self.template_name, context)
