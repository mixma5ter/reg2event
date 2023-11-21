import os
import time


def get_file_version(file_path):
    try:
        modification_time = os.path.getmtime(file_path)
        version = time.strftime('%Y%m%d%H%M%S', time.localtime(modification_time))
        return version
    except Exception as e:
        # В случае ошибки возвращаем дефолтное значение
        return 'unknown'


def version(request):
    file_path = 'static/css/style.css'  # путь к вашему файлу
    return {'STATIC_VERSION': get_file_version(file_path)}
