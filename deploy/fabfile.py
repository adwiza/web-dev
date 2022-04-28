from fabric.api import local, run, sudo
from fabric.api import env, cd
from fabric.contrib import files

env.hosts = ['localhost']
env.user = 'adwiz'
env.password = 'Rangsmit+101+'


def install_packages():
    packages = [
        'ssh',
        'mc',
        'iptraf-ng',
        'git-core'
    ]
    sudo(f'apt install -y {" ".join(packages)}')


def create_venv():
    if not files.exists('/home/adwiz/venv'):
        run('python3 -m venv venv')
    run('pwd')
    run('. venv/bin/activate')


def install_project_code():
    if not files.exists('~/graphql-shop-example'):
        run('git clone https://github.com/VladimirFilonov/graphql-shop-example')
    else:
        with cd('graphql-shop-example'):
            run('git pull')


def install_pip_requirements():
    with cd('graphql-shop-example'):
        run('~/venv/bin/pip install -r requirements.txt --upgrade')


def configure_uwsgi():
    pass


def migrate_database():
    pass


def configure_nginx():
    pass


def restart_all():
    pass


def bootstrap():
    install_packages()
    create_venv()
    install_project_code()
    install_pip_requirements()
    configure_uwsgi()
    configure_nginx()
    migrate_database()
    restart_all()