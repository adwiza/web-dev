from fabric.api import local, run, sudo
from fabric.api import env, cd
from fabric.contrib import files

env.hosts = ['localhost']
env.user = 'adwiz'
env.password = ''


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
    with cd('/home/adwiz/PycharmProjects/web-dev'):
        run('venv/bin/pip install -r requirements.txt --upgrade')


def configure_uwsgi():
    sudo('python3 -m pip install uwsgi')
    sudo('mkdir -p /etc/uwsgi/sites')
    files.upload_template('templates/uwsgi.ini', '/etc/uwsgi/sites/gqlshop.ini', use_sudo=True)
    files.upload_template('templates/uwsgi.service', '/etc/systemd/system/uwsgi.service', use_sudo=True)


def migrate_database():
    with cd('/home/adwiz/PycharmProjects/web-dev'):
        run('venv/bin/python manage.py migrate')


def configure_nginx():
    if files.exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    files.upload_template('templates/nginx.conf', '/etc/nginx/sites-enabled/gqlshop.conf', use_sudo=True)


def restart_all():
    sudo('systemctl daemon-reload')
    sudo('systemctl restart nginx')
    sudo('systemctl restart uwsgi')


def bootstrap():
    install_packages()
    create_venv()
    install_project_code()
    install_pip_requirements()
    configure_uwsgi()
    configure_nginx()
    migrate_database()
    restart_all()
