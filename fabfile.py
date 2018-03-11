"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This script is used to control deployment process and make it as easy as possible for end user.
Please do not forget to set host machine environment variables listed under 'required info'.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os
from fabric.api import local

# REQUIRED INFO
HOST_IP = os.environ['HOST_IP']
APP_NAME = os.environ['APP_NAME']
REPO_URL = os.environ['REPO_URL']
DB_PASS = os.environ['DB_PASS']
APP_REPLICAS = os.environ['APP_REPLICAS']


def init():
    """ use this when deploying the stack for the first time """
    clone_app()
    rename()
    build()
    storage()
    up()


def scale_app(replicas):
    """ use this to temporary tweak replicas count of the 'app service'
    (NOTE: this effect will vanish on next 'stack down' command, use environment variable for permanent set-up) """
    local(f'docker service scale {APP_NAME}_app={replicas}')


def update(type):
    """ use this to update 'stack/app' code base """
    if type == "stack":
        local('git reset --hard && git pull')
    if type == "app":
        local(f'cd app/{APP_NAME} git reset --hard && git pull')
    rename()
    build()
    up()


def clone_app():
    local(f'cd app && mkdir {APP_NAME} && git clone {REPO_URL}')
    local(f'cd app/{APP_NAME}')


def rename():
    local(f'sed -i "s/%replicas: 1%/replicas: {APP_REPLICAS}/" docker-stack.yml')
    local(f'sed -i "s/%APP_NAME%/{APP_NAME}/g" app/Dockerfile app/entry.sh nginx/sites-enabled/django postgres/env')
    local(f'sed -i "s/%DB_PASS%/{DB_PASS}/g" postgres/env')
    local(f'sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = [\'{HOST_IP}\']/" app/{APP_NAME}/{APP_NAME}/settings.py')


def build():
    local('docker build app/. -t my/app')
    local('docker build nginx/. -t my/nginx')


def storage():
    """ there has to be an empty directory for psql persistent storage """
    local('mkdir postgres/storage')


def up():
    """ use this to redeploy the stack after it was removed with 'down'
    or apply any custom changes made in 'docker-stack.yml' file """
    local(f'docker stack deploy --compose-file docker-stack.yml {APP_NAME}')


def down():
    """ use this to remove stack from the host
    (WARNING: will delete all the data inside every container, except data stored directly on host e.g. 'postgres') """
    local(f'docker stack rm {APP_NAME}')
