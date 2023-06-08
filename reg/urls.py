from django.urls import path

from .views import RegView, RegInfoView

app_name = 'reg'

urlpatterns = [
    # Страница регистрации
    path('<int:deal_id>/', RegView.as_view(), name='reg_form'),
    # Страница информации о регистрации
    path('<int:deal_id>/<str:slug>/', RegInfoView.as_view(), name='reg_info'),
]
