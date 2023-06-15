from django.urls import path

from .forms import check_deal_ajax
from .views import FormCreateView, FormUpdateView, FormsListView, IndexView

app_name = 'forms'

urlpatterns = [
    # Главная страница
    path('', IndexView.as_view(), name='index'),
    # Список форм
    path('all/', FormsListView.as_view(), name='form_list'),
    # Добавление новой формы
    path('create/', FormCreateView.as_view(), name='form_create'),
    # Проверка сделки по Ajax запросу
    path('check_deal/<int:deal_id>/', check_deal_ajax, name='check_deal'),
    # Просмотр и редактирование формы
    path('<int:pk>/', FormUpdateView.as_view(), name='form_update'),
]
