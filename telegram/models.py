import telebot
from django.db import models


class TelegramBot(models.Model):
    """Класс телеграм бота."""

    name = models.CharField(
        max_length=255,
        verbose_name='Название бота',
        help_text='Введите название бота',
    )
    token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Токен бота',
        help_text='Введите токен бота',
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Активен',
    )

    def __str__(self):
        return self.token

    def send_message(self, chat_id, message):
        bot = telebot.TeleBot(self.token)
        try:
            bot.send_message(chat_id, message)
            return True
        except telebot.apihelper.ApiTelegramException as e:
            print(f'Ошибка отправки сообщения в Telegram: {e}')
            return False

    class Meta:
        verbose_name = 'Телеграм бот'
        verbose_name_plural = 'Телеграм боты'


def send_form_data_to_telegram(form_obj, request_data):
    """Отправка сообщения в ТГ канал."""

    if form_obj.telegram_channel_id:
        try:
            bot = TelegramBot.objects.get(is_active=True)
        except TelegramBot.DoesNotExist:
            print('Активный бот не найден')
            return

        message = f"-{form_obj.title}-\n\n"

        for field in form_obj.fields.order_by('order_id'):
            value = request_data.get(field.label)
            if value:
                if value == 'on':
                    value = 'Да'
                message += f'{field.label}: {value}\n'

        if bot.send_message(form_obj.telegram_channel_id, message):
            print('Сообщение успешно отправлено в Telegram')
        else:
            print('Ошибка отправки сообщения в Telegram')
