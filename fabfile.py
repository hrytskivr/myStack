"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This script is used to control deployment process and make it as easy as possible for end user.
Please do not forget to set host machine environment variables listed under 'required info'.

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os

from fabric.api import local

""" REQUIRED INFO """
HOST_IP = os.environ['HOST_IP']  # public ip address of your hosting machine
REPO_URL = os.environ['REPO_URL']  # git url of your application repository
REPO_NAME = os.environ['REPO_NAME']  # name of your application repository
APP_NAME = os.environ['APP_NAME']  # name of your Django application
APP_REPLICAS = os.environ['APP_REPLICAS']  # replicas count of Django application service to deploy

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

""" USEFUL CONSTANTS """
COMMIT_HASH = local('git rev-parse --short HEAD', capture=True)


def init():
    """ use this when deploying the stack for the first time """
    clone_app()
    rename()
    build()
    storages()
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
        local(f'cd app/{REPO_NAME} git reset --hard && git pull')
    rename()
    build()
    up()


def clone_app():
    local(f'cd app && mkdir {REPO_NAME} && git clone {REPO_URL}')


def rename():
    local(f'sed -i "s/%app_replicas: 1%/replicas: {APP_REPLICAS}/" docker-stack.yml')
    local(f'sed -i "s/%COMMIT_HASH%/{COMMIT_HASH}/g" docker-stack.yml')
    local(f'sed -i "s/%APP_NAME%/{APP_NAME}/g" app/Dockerfile app/entry.sh nginx/sites-enabled/django')
    local(f'sed -i "s/%DB_NAME%/{DB_NAME}/; s/%DB_USER%/{DB_USER}/; s/%DB_PASS%/{DB_PASS}/" postgres/env')
    local(f'sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = [\'{HOST_IP}\']/" app/{REPO_NAME}/{APP_NAME}/settings.py')


def build():
    local(f'docker build app/. -t my/app:{COMMIT_HASH}')
    local(f'docker build nginx/. -t my/nginx:{COMMIT_HASH}')


def storages():
    """ this creates persistent storage directories for psql and nginx services """
    local('mkdir postgres/storage')
    local('mkdir nginx/logs')


def up():
    """ use this to redeploy the stack after it was removed with 'down'
    or apply any custom changes made in 'docker-stack.yml' file """
    local(f'docker stack deploy --compose-file docker-stack.yml {APP_NAME}')


def down(type):
    """ use this to remove stack from the host """
    if type == '-f':
        print('Forced!')
        local(f'docker stack rm {APP_NAME}')
    else:
        print('echo WARNING: will delete all the data inside every container, '
              'except data stored directly on host e.g. "postgres".')
        choice = input('Proceed? Yes/No\n=> ')
        if choice == 'Yes':
            print('Confirmed!')
            local(f'docker stack rm {APP_NAME}')
        elif choice == 'No':
            print('Aborted!')
        else:
            print('Wrong input! ')
