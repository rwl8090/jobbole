# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''

from flask_script import Manager
from jobbole import app
from flask_migrate import Migrate, MigrateCommand
from app import db

manager = Manager(app)
# 1. 要使用flask_migrate，必须绑定app和db
migrate = Migrate(app, db)
# 2. 把MigrateCommand命令添加到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
