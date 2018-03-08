"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This script is used to control deployment process and make it as easy as possible for end user.
Please do not forget to set host machine environment variables described under 'required info'.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
from fabric.api import local

# REQUIRED INFO
APP_NAME = os.environ['APP_NAME']
REPO_URL = os.environ['REPO_URL']
DB_PASS = os.environ['DB_PASS']


def init():
    """ use this when deploying the stack for the first time """
    clone_app()
    rename()
    build()
    storage()
    up()


def update_app():
    """ use this to update your application code from remote repo """
    local(f'cd app/{APP_NAME} git reset --hard && git pull')
    rename()
    build()
    up()


def update_stack():
    """ use this to update stack code from remote repo """
    local('git reset --hard && git pull')
    rename()
    build()
    up()


def clone_app():
    local(f'cd app && mkdir {APP_NAME} && git clone {REPO_URL}')
    local(f'cd app/{APP_NAME} && git checkout prod')


def rename():
    local(f'sed -i "s/%APP_NAME%/{APP_NAME}/g" app/Dockerfile app/entry.sh nginx/sites-enabled/django postgres/env')
    local(f'sed -i "s/%DB_PASS%/{DB_PASS}/g" postgres/env')


def build():
    local('docker build app/. -t my/app')
    local('docker build nginx/. -t my/nginx')

def storage():
    """ there has to be an empty directory for psql persistent storage """
    local('mkdir postgres/storage')

def up():
    """ use this to redeploy the stack after it was removed with 'down' """
    local(f'docker stack deploy --compose-file docker-compose.yml {APP_NAME}')


def down():
    """ use this to remove stack from the host
    (WARNING: will delete all the data inside every container) """
    local(f'docker stack rm {APP_NAME}')
