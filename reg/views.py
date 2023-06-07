from django.shortcuts import get_object_or_404, render
from django.views import View

from core.bitrix import create_element
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
        reg_form = self.form_class(request.POST, deal_id=deal_id)
        if reg_form.is_valid():
            form = get_object_or_404(Form, deal_id=deal_id)

            fields = {'NAME': 'Регистрация'}
            for field in form.fields.all():
                key = field.bitrix_id
                value = request.POST.get(field.label)
                if value:
                    fields[key] = value

            # Создание нового элемента в Битрикс
            response = create_element(deal_id, fields)
            if response.ok:
                stream_link = get_object_or_404(Form, deal_id=deal_id).stream_link
                context = {
                    'title': 'Регистрация успешно завершена',
                    'stream_link': stream_link,
                }
                return render(request, 'reg/reg_done.html', context)
            else:
                context = {'title': 'Возникла ошибка при регистрации'}
                return render(request, 'reg/reg_done.html', context)

        else:
            context = {
                'title': self.title,
                'form': reg_form,
                'errors': reg_form.errors.items()
            }
            return render(request, self.template_name, context)
