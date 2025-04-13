from django.contrib import admin

from .models import TelegramBot


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    """Регистрация модели телеграм бота в админке."""

    save_on_top = True
    list_select_related = True
    empty_value_display = '-пусто-'
    list_display = (
        'pk',
        'name',
        'token',
        'is_active',
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
