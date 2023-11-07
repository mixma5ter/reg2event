from django.contrib import admin

from .models import BasicField, Group, Form, Field, FieldChoice


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Регистрация модели группы для формы в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'name',
        'pub_date',
        'update_date',
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


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
        'group',
        'deal_title',
        'form_link',
        'stream_link',
        'end_date',
        'pub_date',
        'update_date',
    )
    list_display_links = ('deal_id', 'title',)
    search_fields = ('deal_id', 'title',)
    list_filter = ('author', 'group',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    """Регистрация модели поля формы в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'order_id',
        'label',
        'field_type',
        'form',
        'is_active',
        'bitrix_id',
        'pub_date',
        'update_date',
    )
    list_display_links = ('label',)
    list_editable = ('order_id',)
    search_fields = ('label', 'form',)
    list_filter = ('form',)
    ordering = ('order_id',)


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
        'order_id',
        'label',
        'visible',
        'field_type',
        'default',
        'pub_date',
        'update_date',
    )
    list_display_links = ('label',)
    list_editable = ('order_id', 'visible', 'default',)
    search_fields = ('label',)
    list_filter = ('visible',)
    ordering = ('order_id',)
