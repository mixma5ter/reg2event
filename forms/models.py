from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()

FIELD_TYPE_CHOICES = [
    ('text', 'Text'),
    ('textarea', 'Textarea'),
    ('number', 'Number'),
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('checkbox', 'Checkbox'),
    ('radio', 'Radio'),
    ('select', 'Select'),
]


def getUser():
    """Callable function."""
    return User.objects.get_or_create(username=User)


class Form(CreatedModel):
    """Модель формы регистрации на мероприятие."""

    deal_id = models.IntegerField(
        db_index=True,
        unique=True,
        verbose_name='ID мероприятия',
        help_text='Введите ID мероприятия'
    )
    deal_title = models.CharField(
        max_length=255,
        verbose_name='Название сделки',
        help_text='Введите название сделки',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET(getUser),
        related_name='posts',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название формы',
        help_text='Введите название формы',
    )
    end_date = models.DateTimeField(
        verbose_name='Дата окончания регистрации',
    )
    stream_link = models.CharField(
        max_length=255,
        verbose_name='Ссылка на трансляцию',
        blank=True,
        null=True,
    )
    form_link = models.CharField(
        max_length=255,
        verbose_name='Ссылка на форму',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Форма регистрации'
        verbose_name_plural = 'Формы регистрации'

    def __str__(self):
        res = f'{self.deal_id} - {self.title}'
        return res


class Field(CreatedModel):
    """Модель поля формы регистрации."""

    label = models.CharField(
        max_length=255,
        verbose_name='Название поля',
        help_text='Введите название поля'
    )
    field_type = models.CharField(
        max_length=255,
        choices=FIELD_TYPE_CHOICES,
        verbose_name='Тип поля',
        help_text='Выберите тип поля'
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='fields',
        verbose_name='Форма',
        help_text='Выберите форму'
    )
    is_active = models.BooleanField(
        default=None,
        verbose_name='Добавить поле в форму',
        help_text='Поставьте галочку если нужно добавить поле в форму'
    )
    bitrix_id = models.CharField(
        max_length=255,
        verbose_name='Битрикс ID',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Поле формы'
        verbose_name_plural = 'Поля формы'

    def __str__(self):
        res = f'{self.form.deal_id} - {self.label}'
        return res


class FieldChoice(CreatedModel):
    """Модель поля выбора Select."""

    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,
        related_name='choices',
    )
    choice_text = models.CharField(
        max_length=255,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Поле выбора'
        verbose_name_plural = 'Поля выбора'

    def __str__(self):
        return self.choice_text


class BasicField(CreatedModel):
    """Модель базового поля."""

    label = models.CharField(
        max_length=255,
        verbose_name='Название поля',
        help_text='Введите название поля'
    )
    field_type = models.CharField(
        max_length=255,
        choices=FIELD_TYPE_CHOICES,
        verbose_name='Тип поля',
        help_text='Выберите тип поля'
    )
    order_id = models.IntegerField(
        verbose_name='Порядковый номер',
        help_text='Введите порядковый номер'
    )
    visible = models.BooleanField(
        verbose_name='Видимое'
    )
    default = models.BooleanField(
        default=False,
        verbose_name='Включено по умолчанию'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Базовое поле'
        verbose_name_plural = 'Базовые поля'

    def __str__(self):
        return self.label
