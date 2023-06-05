import requests

from config.settings import WEB_HOOK

IBLOCK_TYPE_ID = 'lists_socnet'
IBLOCK_CODE = 'registration_{}'  # код информационного блока
SOCNET_GROUP_ID = 16


def request(command, event_id, fields):
    url = WEB_HOOK + command
    params = {
        'IBLOCK_TYPE_ID': IBLOCK_TYPE_ID,
        'SOCNET_GROUP_ID': SOCNET_GROUP_ID,
        'IBLOCK_CODE': IBLOCK_CODE.format(event_id)
    }
    if fields:
        params['fields'] = fields
    return requests.post(url, json=params)
