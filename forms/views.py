from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView

from .models import RegForm

CARDS_ON_PAGE = 6


class IndexView(ListView):
    """Главная страница."""

    template_name = 'forms/index.html'
    context_object_name = 'forms'
    title = 'Регистрация обращений'

    def get_queryset(self):
        cards = RegForm.objects.all().order_by('-pub_date')[:CARDS_ON_PAGE]
        return cards

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['title'] = self.title
        context['cards'] = self.get_queryset()
        return context
