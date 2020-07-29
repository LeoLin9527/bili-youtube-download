"""
@file:manage.py
@time:2020/7/26-19:57
"""
from flask_script import Manager, Server

from app import app

manager = Manager(app)


# 创建命令
@manager.command
def print_str():
    print('hello world!')


manager.add_command('runserver', Server(host='0.0.0.0', port=5555, use_debugger=True))

if __name__ == '__main__':
    # 通过管理对象启动flask
    manager.run()
