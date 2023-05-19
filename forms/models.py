from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def getUser():
    """Callable function."""
    return User.objects.get_or_create(username=User)


class RegForm(models.Model):
    """Модель формы регистрации на мероприятие."""

    deal_id = models.IntegerField(
        db_index=True,
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
    fields = models.TextField(
        blank=True,
        verbose_name='Список полей',
        help_text='Введите список полей через запятую',
    )
    event_date = models.DateField(
        verbose_name='Дата мероприятия',
        help_text='Выберите дату мероприятия',
    )
    pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    update_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Форма регистрации'
        verbose_name_plural = 'Формы регистрации'

    def __str__(self):
        return self.title
