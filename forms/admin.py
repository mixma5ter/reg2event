from django.contrib import admin

from .models import BasicField, Form, Field, FieldChoice


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Регистрация модели формы в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'deal_id',
        'author',
        'title',
        'deal_title',
        'form_link',
        'stream_link',
        'end_date',
        'pub_date',
        'update_date',
    )
    list_display_links = ('deal_id', 'title',)
    search_fields = ('deal_id', 'title',)
    list_filter = ('author',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    """Регистрация модели поля формы в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
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
class FieldChoiceAdmin(admin.ModelAdmin):
    """Регистрация модели поля выбора в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'field',
        'choice_text',
        'pub_date',
        'update_date',
    )
    list_display_links = ('choice_text',)
    search_fields = ('field', 'choice_text',)


@admin.register(BasicField)
class BasicFieldAdmin(admin.ModelAdmin):
    """Регистрация модели поля формы в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'label',
        'field_type',
        'order_id',
        'visible',
        'default',
        'pub_date',
        'update_date',
    )
    list_display_links = ('label', 'order_id',)
    search_fields = ('label',)
    list_filter = ('visible',)
