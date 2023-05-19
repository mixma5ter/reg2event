from django.contrib import admin

from .models import RegForm


class MyAdmin(admin.ModelAdmin):
    """Переопределение общих параметров для всех моделей админки."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'

    class Meta:
        abstract = True


@admin.register(RegForm)
class FormAdmin(MyAdmin):
    """Регистрация модели конкурса в админке."""

    list_display = (
        'pk',
        'deal_id',
        'author',
        'title',
        'fields',
        'event_date',
        'pub_date',
        'update_date',
    )
    list_display_links = ('deal_id', 'title',)
    search_fields = ('deal_id', 'title',)
    list_filter = ('author', 'event_date',)
