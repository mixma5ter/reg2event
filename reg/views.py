from django.shortcuts import get_object_or_404, render
from django.views import View

from forms.models import Form


class RegView(View):
    template_name = 'reg/reg_form.html'

    def get(self, request, deal_id):
        # Получаем модель формы по ID
        reg_form = get_object_or_404(Form, deal_id=deal_id)
        # Получаем поля формы связанные с формой
        reg_fields = reg_form.fields.all().filter(is_active=True).order_by('pk')
        context = {
            'reg_form': reg_form,
            'reg_fields': reg_fields,
        }
        return render(request, self.template_name, context)
