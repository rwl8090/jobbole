# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 数据库操作
'''

from app import db

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