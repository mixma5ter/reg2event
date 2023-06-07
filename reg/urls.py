from django.urls import path

from .views import RegView, RegDoneView, RegErrorView

app_name = 'reg'

urlpatterns = [
    # Страница регистрации
    path('<int:deal_id>/', RegView.as_view(), name='reg_form'),
    path('<int:deal_id>/done/', RegDoneView.as_view(), name='reg_done'),
    path('<int:deal_id>/error/', RegErrorView.as_view(), name='reg_error'),
]
