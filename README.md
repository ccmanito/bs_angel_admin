bs_angel-admin

============

## Install dependency

    # yum install -y python-virtualenv

    $ cd bs_angel_admin/

    $ pip install virtualenv

    $ virtualenv -p /usr/bin/python3.6  ./.venv

    $ source ./.venv/bin/activate

    $ ./.venv/bin/pip install -r pip_requirements.txt

### 启动项目

    # source env/bin/activate
    # python manage.py runserver 127.0.0.1:8080
