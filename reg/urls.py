from django.urls import path

from .views import RegView

app_name = 'reg'

urlpatterns = [
    # Страница регистрации
    path('<int:deal_id>/', RegView.as_view(), name='reg_form'),
]
