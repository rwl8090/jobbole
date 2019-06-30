# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 测试
'''
import unittest


from app import db, create_app
from app.models import User, Role


class test_model_TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()



    def test_valid_confirmation_token(self):
        u = User(user_passwd='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))



tt1 = test_model_TestCase()
tt1.setUp()
tt1.test_valid_confirmation_token()

