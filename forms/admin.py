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
    """Регистрация модели формы в админке."""

    list_display = (
        'pk',
        'deal_id',
        'author',
        'title',
        'deal_title',
        'stream_link',
        'form_link',
        'pub_date',
        'update_date',
    )
    list_display_links = ('deal_id', 'title',)
    search_fields = ('deal_id', 'title',)
    list_filter = ('author',)


@admin.register(Field)
class FieldAdmin(MyAdmin):
    """Регистрация модели поля формы в админке."""

    list_display = (
        'pk',
        'label',
        'field_type',
        'form',
        'is_active',
        'bitrix_id',
        'pub_date',
        'update_date',
    )
    list_display_links = ('label',)
    search_fields = ('label', 'form',)
    list_filter = ('form',)


@admin.register(FieldChoice)
class FieldChoiceAdmin(MyAdmin):
    """Регистрация модели поля выбора в админке."""

    list_display = (
        'pk',
        'field',
        'choice_text',
        'pub_date',
        'update_date',
    )
    list_display_links = ('choice_text',)
    search_fields = ('field', 'choice_text',)
