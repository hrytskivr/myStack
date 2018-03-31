"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This script is used to control deployment process and make it as easy as possible for end user.
It is divided into 4 sections:
    - REQUIRED INFO (environment variables that must be set on host machine before deployment)
    - MAIN FLOW (this is the main flow of the deployment process)
    - CONTROL COMMANDS (user can control his stack with this commands after deployment)
    - CONSTANTS & UTILS (various constants & helper functions - to stick with DRY principles)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os

from fabric.api import local
from fabric.context_managers import lcd

### REQUIRED INFO ###
HOST_IP = os.environ['HOST_IP']  # public ip address of your hosting machine
REPO_URL = os.environ['REPO_URL']  # git url of your application repository
REPO_NAME = os.environ['REPO_NAME']  # name of your application repository
APP_NAME = os.environ['APP_NAME']  # name of your Django application

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']


### MAIN FLOW ###
def init():
    """ run this when deploying the stack for the first time """
    clone_app()
    insert_variables()
    generate_tls()
    create_storages()
    create_network()
    deploy_registry()
    make_images()
    up()


def clone_app():
    """ this will clone your Django application """
    with lcd('app'):
        local(f'mkdir {REPO_NAME} && git clone {REPO_URL}')


def insert_variables():
    """ this will replace template placeholders with provided info """
    local(f'sed -i "s/%COMMIT_HASH%/{get_hash()}/g" docker-stack.yml')
    local(f'sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = [\'{HOST_IP}\']/" app/{REPO_NAME}/{APP_NAME}/settings.py')
    local(f'sed -i "s/%DB_NAME%/{DB_NAME}/; s/%DB_USER%/{DB_USER}/; s/%DB_PASS%/{DB_PASS}/" postgres/env')
    local(f'sed -i "s/%REGISTRY_URL%/{REGISTRY_URL}/g" docker-stack.yml')
    local(f'sed -i "s/%APP_NAME%/{APP_NAME}/g" app/Dockerfile '
                                              'app/app.sh '
                                              'registry/registry.sh '
                                              'nginx/sites-enabled/django '
                                              'docker-stack.yml')


def generate_tls():
    """ this will run the script which will generate tls keys & certificates for nginx & registry services """
    with lcd('tls'):
        local('sh tls.sh')


def create_storages():
    """ this will create persistent storage directories for postgres, nginx & registry services """
    local('mkdir postgres/data')
    local('mkdir nginx/logs')
    local('mkdir registry/store')


def create_network():
    """ this will create encrypted & attachable overlay network """
    local(f'docker network create --opt encrypted --driver overlay --attachable {APP_NAME}_network')


def deploy_registry():
    """ this will run the script which will run docker registry container """
    with lcd('registry'):
        local('sh registry.sh')


def make_images():
    """ this will build & push docker images to the registry """
    local(f'docker build app/. -t {REGISTRY_URL}/app:{get_hash()} && '
          f'docker push {REGISTRY_URL}/app:{get_hash()}')
    local(f'docker build nginx/. -t {REGISTRY_URL}/nginx:{get_hash()} && '
          f'docker push {REGISTRY_URL}/nginx:{get_hash()}')


### CONTROL COMMANDS ###
def up():
    """ use this to bring up the stack after it was removed with 'down' command
    or apply any custom changes made in 'docker-stack.yml' file """
    local(f'docker stack deploy --compose-file docker-stack.yml {APP_NAME}')


def down(type):
    """ use this to stop & remove the stack """
    if type == "-f":
        print('\nForced!')
        local(f'docker stack rm {APP_NAME}')
    else:
        print('\nWARNING: will delete all the data inside every container, '
              'except that are stored as persistent storage e.g. "postgres".')
        choice = input('\nProceed? Yes/No\n=> ')
        if choice == 'Yes':
            print('\nConfirmed!')
            local(f'docker stack rm {APP_NAME}')
        elif choice == 'No':
            print('\nAborted!')
        else:
            print('\nWrong input! ')


def scale(service, replicas):
    """ use this to temporary tweak replicas count of the given service """
    print('\nNOTE: this setting will only last until next "down" command!')
    local(f'docker service scale {APP_NAME}_{service}={replicas}')


def update(type):
    """ use this to update code base either for 'myStack' or your Django application """
    if type == "stack":
        local('git reset --hard && git pull')
    if type == "app":
        with lcd(f'app/{REPO_NAME}'):
            local(f'git reset --hard && git pull')
    insert_variables()
    make_images()
    up()


def status():
    """ use this to get stack services status, escape with Ctrl+C """
    local('watch docker service ls')


### CONSTANTS & UTILS ###
REGISTRY_URL = '127.0.0.1:5000'


def get_hash():
    """ return last git commit hash """
    return local('git rev-parse --short HEAD', capture=True)
