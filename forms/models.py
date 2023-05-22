from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel

User = get_user_model()


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
    author = models.ForeignKey(
        User,
        on_delete=models.SET(getUser),
        related_name='posts',
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название мероприятия',
        help_text='Введите название мероприятия',
    )
    event_date = models.DateField(
        verbose_name='Дата мероприятия',
        help_text='Выберите дату мероприятия',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Форма регистрации'
        verbose_name_plural = 'Формы регистрации'

    def __str__(self):
        return self.title


class Field(CreatedModel):
    """Модель поля формы регистрации."""

    FIELD_TYPE_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio'),
        ('select', 'Select'),
    ]
    label = models.CharField(
        max_length=255,
    )
    field_type = models.CharField(
        max_length=255,
        choices=FIELD_TYPE_CHOICES,
    )
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
        related_name='fields',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Поле формы'
        verbose_name_plural = 'Поля формы'

    def __str__(self):
        return self.label


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
