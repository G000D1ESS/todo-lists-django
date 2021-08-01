import random
import string

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = "https://github.com/G000D1ESS/tdd-book.git"


def deploy():
    '''Развернуть сервер'''
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    '''Создать структру каталога, если нужно'''
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    '''Получить самый свежий исходный код'''
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    run(f'cd {source_folder} && git reset --hard')


def _update_settings(source_folder, site_name):
    '''Обновить настройки'''
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWED_HOSTS =.+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        run(f'cd {source_folder}/superlists && touch secret_key.py')
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()[]^'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, 'from .secret_key import SECRET_KEY') 


def _update_virtualenv(source_folder):
    '''Обновить виртулаьную среду'''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.7 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    '''Обновить статические файлы'''
    run(f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    '''Обновить базу данных'''
    run(f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput')
