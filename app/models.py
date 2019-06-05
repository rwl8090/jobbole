# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 数据模型层
'''
from app import db

# 数据库类
class Role(db.Model):
    __tablename__ = 'role'  # 指定表名
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True)
    user = db.relationship('User', backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def __repr__(self):
        return '<User %r>' % self.user_name

