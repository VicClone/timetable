# -*- coding: utf-8 -*-
from fabric.api import task
from fabric.api import run
from fabric.api import local
from fabric.api import hosts, env
from fabric.api import cd
from fabric.api import prefix
from fabric.api import shell_env
from fabric.operations import require


# ==============================================================================
# Deploy
# ==============================================================================


STAGES = {
    'production': {
        'user': 'user',
        'hosts': ['ceramic@interiorforyou.ru:54022'],
        'branch': 'master',
        'docker_file': 'docker-compose.production.yml',
        'root_dir': '/home/ceramic/muskrat',
    },
    'staging': {
        'user': 'deniska',
        'hosts': ['deniska@37.98.245.58:55872'],
        'host_string': '37.98.245.58:55872',
        'branch': 'develop',
        'docker_file': 'docker-compose.staging.yml',
        'root_dir': '/home/deniska/muskrat',
    },

}


def stage_set(stage_name='test'):
    env.stage = stage_name
    env.use_ssh_config = True
    for option, value in STAGES[env.stage].items():
        setattr(env, option, value)


@task
def production():
    stage_set('production')


@task
def staging():
    stage_set('staging')


@task
def stage_deploy():
    stage_set('staging')
    require('stage', provided_by=(production, staging))

    with shell_env(COMPOSE_FILE=env.docker_file, COMPOSE_HTTP_TIMEOUT='300'):
        with cd(env.root_dir):
            run('git fetch origin %s' % env.branch)
            run('git checkout %s' % env.branch)
            run('git pull origin %s' % env.branch)
            run('docker-compose down')
            run('docker-compose up -d')
            run('docker-compose exec backend pip install -r requirements/staging.txt')
            run('docker-compose exec backend python manage.py migrate')
            run('docker-compose exec backend python manage.py collectstatic --noinput')
            run('docker-compose exec nodejs9 npm i')
            run('docker-compose -f %s build' % env.docker_file)
            run('docker-compose down')
            run('docker-compose -f %s down' % env.docker_file)
            run('docker-compose -f %s up -d' % env.docker_file)


@task
def collectstatic():
    local('docker-compose exec backend python manage.py collectstatic --noinput')


@task
def restart():
    with shell_env(COMPOSE_FILE=env.docker_file, COMPOSE_HTTP_TIMEOUT='300'):
        with cd(env.root):
            run('docker-compose down')
            run('docker-compose up -d')


# ==============================================================================
# Docker
# ==============================================================================

@task
def build():
    local('docker-compose build')


@task
def start(port='8000'):
    with prefix('export APP_PORT=%s' % port):
        with shell_env(COMPOSE_HTTP_TIMEOUT='300'):
            local('docker-compose up -d')


@task
def stop():
    local('docker-compose down')


@task
def status():
    local('docker-compose ps')


@task
def migrate(app='', fake=False):
    local('docker-compose exec backend python manage.py migrate %s %s' % (
        app,
        '--fake-initial' if fake else ''
    ))


@task
def makemigrations(app=''):
    local('docker-compose exec backend python manage.py makemigrations %s' % app)


@task
def runserver():
    local('docker-compose exec backend python manage.py runserver 0.0.0.0:8000')


@task
def createsuperuser():
    local('docker-compose exec backend python manage.py createsuperuser')


@task
def shell():
    local('docker-compose exec backend python manage.py shell')


@task
def shell_plus():
    local('docker-compose exec backend python manage.py shell_plus')


@task
def sqlshell():
    local('docker-compose exec backend python manage.py shell_plus --print-sql')


@task
def run_tests(app=''):
    local('docker-compose exec backend python manage.py test %s --keepdb' % app)


@task
def manage(command):
    local('docker-compose exec backend python manage.py %s' % command)


@task
def psql(database=''):
    local("docker-compose exec backend_db su postgres -c 'psql %s'" % database)


@task
def restart():
    local('docker-compose restart')


@task
def npm_i(args=''):
    local('docker-compose exec nodejs9 npm i %s' % args)


@task
def run_dev(args=''):
    local('docker-compose exec nodejs9 npm run dev')


@task
def run_watch(args=''):
    local('docker-compose exec nodejs9 npm run watch')


@task
def imprt_cities(args=''):
    local('docker-compose exec backend python manage.py cities')
