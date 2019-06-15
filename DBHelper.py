# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 数据库操作
'''

from app import db
from app.models import User

class DBHelper(object):

    def add_data(self, data):
        '''新增数据'''
        try:
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def login_check(self, login_name, user_passwd):
        '''登录验证'''
        user = User.query.filter_by(user_login_name=login_name).first_or_404()
        if user.check_passwd_hash(user_passwd):
            return True
        else:
            return False