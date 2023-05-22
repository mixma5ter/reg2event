from django.contrib import admin

from .models import Form, Field, FieldChoice


class MyAdmin(admin.ModelAdmin):
    """Переопределение общих параметров для всех моделей админки."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'

    class Meta:
        abstract = True


@admin.register(Form)
class FormAdmin(MyAdmin):
    """Регистрация модели конкурса в админке."""

    list_display = (
        'pk',
        'deal_id',
        'author',
        'title',
        'event_date',
        'pub_date',
        'update_date',
    )
    list_display_links = ('deal_id', 'title',)
    search_fields = ('deal_id', 'title',)
    list_filter = ('author', 'event_date',)


@admin.register(Field)
class FieldAdmin(MyAdmin):
    """Регистрация модели конкурса в админке."""

    list_display = (
        'pk',
        'label',
        'field_type',
        'form',
        'pub_date',
        'update_date',
    )
    list_display_links = ('label',)
    search_fields = ('label', 'form',)
    list_filter = ('form',)


@admin.register(FieldChoice)
class FieldChoiceAdmin(MyAdmin):
    """Регистрация модели конкурса в админке."""

    list_display = (
        'pk',
        'field',
        'choice_text',
        'pub_date',
        'update_date',
    )
    list_display_links = ('choice_text',)
    search_fields = ('field', 'choice_text',)
