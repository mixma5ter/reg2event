import uuid

import requests
from transliterate import slugify

from config.settings import WEB_HOOK

IBLOCK_TYPE_ID = 'lists_socnet'
IBLOCK_CODE = 'registration_{}'  # код информационного блока
SOCNET_GROUP_ID = 16


def request(command, event_id, fields):
    """Делает запрос к Битрикс-API."""

    url = WEB_HOOK + command
    params = {
        'IBLOCK_TYPE_ID': IBLOCK_TYPE_ID,
        'SOCNET_GROUP_ID': SOCNET_GROUP_ID,
        'IBLOCK_CODE': IBLOCK_CODE.format(event_id)
    }
    if fields:
        params['FIELDS'] = fields
    # права доступа
    if command == 'lists.add':
        params['RIGHTS'] = {
            'AU': 'R',  # авторизованные пользователи - чтение
            'CR': 'X',  # создатель - полный доступ
            'D42': 'W',  # сотрудники отдела - изменение
        }
    return requests.post(url, json=params)


def get_deal(deal_id):
    """Получает сделку из Битрикс по id."""

    command = 'crm.deal.get'
    url = WEB_HOOK + command
    payload = {'id': deal_id}
    return requests.post(url, json=payload)


def check_deal(deal_id):
    """Проверка доступности регистрации."""

    response = get_deal(deal_id)
    data = response.json()
    result = {
        'status': response.status_code,
        'result': data.get('result'),
        'closed': True if data['result']['CLOSED'] == 'Y' else False,
        'errors': data.get('error'),
    }
    return result


def create_list(event, name):
    """Создает список name с событием event в Битрикс. Возвращает id списка."""

    command = 'lists.add'
    fields = {
        'NAME': name,
        'DESCRIPTION': 'Список регистрации на мероприятие',
        'BIZPROC': 'Y',
    }
    result = request(command, event, fields)
    return result.json().get('result')


def delete_list(event):
    """Удаляет список event в Битрикс. Возвращает True если удаление удачно."""

    command = 'lists.delete'
    result = request(command, event, None)
    return result.json().get('result')


def create_field(event, name):
    """Создает поле name в списке event в Битрикс. Возвращает id поля."""

    command = 'lists.field.add'
    translit_name = slugify(name, language_code='ru').replace('-', '_')
    fields = {
        'NAME': name,
        'TYPE': 'S',
        'IS_REQUIRED': 'N',
        'SORT': 1000,
        'CODE': 'field_{}'.format(translit_name),
    }
    result = request(command, event, fields)
    return result.json().get('result')


def delete_field(event, field_id):
    """Удаляет поле name в списке event в Битрикс. Возвращает True если удаление удачно."""

    command = 'lists.field.delete'
    url = WEB_HOOK + command
    params = {
        'IBLOCK_TYPE_ID': IBLOCK_TYPE_ID,
        'SOCNET_GROUP_ID': SOCNET_GROUP_ID,
        'IBLOCK_CODE': IBLOCK_CODE.format(event),
        'FIELD_ID': field_id
    }
    result = requests.post(url, json=params)
    return result.json().get('result')


def create_element(event, fields):
    """Создает элемент в списке event в Битрикс."""

    command = 'lists.element.add'
    url = WEB_HOOK + command
    params = {
        'IBLOCK_TYPE_ID': IBLOCK_TYPE_ID,
        'SOCNET_GROUP_ID': SOCNET_GROUP_ID,
        'IBLOCK_CODE': IBLOCK_CODE.format(event),
        'ELEMENT_CODE': uuid.uuid1().int,
        'FIELDS': fields
    }
    return requests.post(url, json=params)
