from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from core.paginator import paginator
from .models import Form

CARDS_ON_INDEX_PAGE = 6


class IsUserAuthorized(LoginRequiredMixin):
    """Проверка авторизации пользователя."""

    class Meta:
        login_url = 'login'

        def dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)


class IndexView(IsUserAuthorized, ListView):
    """Главная страница."""

    model = Form
    template_name = 'forms/index.html'
    context_object_name = 'forms'
    title = 'Формы регистраций'

    def get_queryset(self):
        cards = Form.objects.all().order_by('-pub_date')[:CARDS_ON_INDEX_PAGE]
        return cards

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title'] = self.title
        context['cards'] = self.get_queryset()
        return context


class FormsListView(IsUserAuthorized, ListView):
    """Страница со списком форм регистрации."""

    model = Form
    template_name = 'forms/forms_list.html'
    context_object_name = 'forms'
    title = 'Формы регистраций'

    def get_queryset(self):
        return Form.objects.all().order_by('-pub_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title'] = self.title
        context['page_obj'], context['page_numbers'] = paginator(self.request, self.get_queryset())
        return context
