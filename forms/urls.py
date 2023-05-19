from django.urls import path

from .views import IndexView

app_name = 'forms'

urlpatterns = [
    # Главная страница
    path('', IndexView.as_view(), name='index'),
]
