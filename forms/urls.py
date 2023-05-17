from django.urls import path

from . import views

app_name = 'forms'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Список форм
    # path('forms/', views.forms_list, name='forms_list'),
    # Просмотр и редактирование формы
    # path('forms/<int:form_id>/', views.form_detail, name='form_detail'),
    # Добавление новой формы
    # path('create/', views.create_form, name='create_form'),
]
