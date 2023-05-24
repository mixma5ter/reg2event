from django.urls import path

from .views import FormCreateView, FormsListView, IndexView

app_name = 'forms'

urlpatterns = [
    # Главная страница
    path('', IndexView.as_view(), name='index'),
    # Список форм
    path('all/', FormsListView.as_view(), name='forms_list'),
    # Просмотр и редактирование формы
    # path('<int:form_id>/', views.form_detail, name='form_detail'),
    # Добавление новой формы
    # path('create/', form_create, name='form_create'),
    path('create/', FormCreateView.as_view(), name='form_create'),
]
