# bs_angel-admin

============

## 环境搭建

### Python版本定为3.5.4  兼容七牛云SDK

### Install dependency on linux

`yum install -y python-virtualenv`

`cd bs_angel_admin/`

`pip install virtualenv`

`virtualenv -p /usr/bin/python3.5.4  ./.venv`

`source ./.venv/bin/activate`

`./.venv/bin/pip install -r requirements.txt`

### Install dependency on windows

`安装Python3.5.4`

`安装 virtualenv： pip install virtualenv`

`virtualenv ./.venv`

`.\.venv\Scripts\activate`

`.\.venv\Scripts\pip install -r requirements.txt`

## 启动项目

### Linux下
 `source env/bin/activate`
### windows下：
`.\.venv\Scripts\activate`

`python manage.py runserver 0.0.0.0:7080`
