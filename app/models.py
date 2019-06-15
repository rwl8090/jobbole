# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 数据模型层
'''
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import manager

# 数据库类
class Role(db.Model):
    __tablename__ = 'role'  # 指定表名
    role_id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    role_name = db.Column(db.String(50), unique=True, comment='角色名称')
    user = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, comment='用户ID')
    user_name = db.Column(db.String(50), comment='用户名')
    user_mbl_nm = db.Column(db.String(20), unique=True, comment='用户电话')
    user_passwd_hash = db.Column(db.String(255), comment='用户密码')
    user_login_name = db.Column(db.String(30), comment='登录名', unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def __repr__(self):
        return '<User %r>' % self.user_login_name

    @property
    def user_passwd(self):
        raise AttributeError('密码不可读')

    @user_passwd.setter
    def user_passwd(self, passwd):
        '''转换密码入库'''
        self.user_passwd_hash = generate_password_hash(passwd)

    def check_passwd_hash(self, passwd):
        '''校对密码'''
        return check_password_hash(self.user_passwd_hash, passwd)

    def get_id(self):
        return (self.user_id)


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))