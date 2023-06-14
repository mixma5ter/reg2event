from django.shortcuts import get_object_or_404, render, redirect
from django.views import View

from core.bitrix import check_deal, create_element
from forms.models import Form
from reg.forms import RegForm


class RegView(View):
    """Страница регистрации пользователей на мероприятие."""

    model = Form
    form_class = RegForm
    template_name = 'reg/reg_form.html'
    context_object_name = 'reg'

    def get(self, request, deal_id):

        reg_info = check_deal(deal_id)
        if reg_info['errors']:
            return redirect('reg:reg_info', deal_id=deal_id, slug='error')
        elif reg_info['closed']:
            return redirect('reg:reg_info', deal_id=deal_id, slug='closed')

        title = get_object_or_404(Form, deal_id=deal_id).title
        reg_form = self.form_class(deal_id=deal_id)
        context = {
            'title': title,
            'form': reg_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, deal_id):

        reg_info = check_deal(deal_id)
        if reg_info['errors']:
            return redirect('reg:reg_info', deal_id=deal_id, slug='error')
        elif reg_info['closed']:
            return redirect('reg:reg_info', deal_id=deal_id, slug='closed')

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

            # Создание нового элемента в Битрикс TODO
            session = request.session.session_key

            response = create_element(deal_id, session, fields)
            if response.ok:
                return redirect('reg:reg_info', deal_id=deal_id, slug='success')
            else:
                return redirect('reg:reg_info', deal_id=deal_id, slug='error')

        else:
            context = {
                'title': self.title,
                'form': reg_form,
                'errors': reg_form.errors.items()
            }
            return render(request, self.template_name, context)


class RegInfoView(View):
    """Страница информации о регистрации."""

    model = Form
    template_name = 'reg/reg_info.html'
    context_object_name = 'reg'

    def get(self, request, deal_id, slug):
        title = 'Регистрация прошла успешно'
        stream_link = get_object_or_404(Form, deal_id=deal_id).stream_link
        if not stream_link.startswith('http'):
            stream_link = 'https://' + stream_link + '/'
        new_reg = True

        if slug == 'closed':
            title = 'Регистрация закрыта'
            new_reg = False
        elif slug == 'error':
            title = 'Возникла ошибка при регистрации'
            stream_link = None

        context = {
            'deal_id': deal_id,
            'title': title,
            'stream_link': stream_link,
            'new_reg': new_reg,
        }
        return render(request, self.template_name, context)
