import random
import uuid

from django.core.management import BaseCommand

from forms.models import Form, Field, User

BASIC_FIELDS = [
    {'ФИО': 'text'},
    {'Организация': 'text'},
    {'Должность': 'text'},
    {'Почта': 'email'},
    {'Телефон': 'phone'},
    {'Комментарий': 'textarea'}
]


class Command(BaseCommand):
    help = 'Создает несколько тестовых форм с базовыми полями.'

    def handle(self, *args, **options):
        template = 'Тестовая регистрация на мероприятие'
        uploaded = 0

        for _ in range(8):
            try:
                deal_id = str(uuid.uuid1().int)[:random.randrange(4, 6)]
                Form.objects.get_or_create(
                    deal_id=deal_id,
                    author=random.choice(User.objects.all()),
                    title=template,
                    form_link=f'/reg/{deal_id}',
                    stream_link=f'http://example.stream.link.com',
                )
                form_id = Form.objects.latest('id').pk
                fields = [
                    Field(label=label, field_type=field_type, form_id=form_id,
                          is_active=random.choice(['True', 'False'])) for
                    field_data in BASIC_FIELDS for label, field_type in field_data.items()]
                Field.objects.bulk_create(fields)
                uploaded += 1
            except:
                pass

        message = f'\nЗагружено - {uploaded} форм.'

        self.stdout.write(self.style.SUCCESS(message))
