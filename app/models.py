# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 数据模型层
'''
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

# class AnonymousUser(AnonymousUserMixin):
#     # confirmed = False
#     @property
#     def confirmed(self):
#         return False


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
    user_name = db.Column(db.String(50), unique=True, comment='用户名')
    user_email = db.Column(db.String(20), unique=True, comment='邮箱')
    user_mbl_nm = db.Column(db.String(20), unique=True, comment='用户电话')
    user_passwd_hash = db.Column(db.String(255), comment='用户密码')
    #user_login_name = db.Column(db.String(30), comment='登录名', unique=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    confirmed = db.Column(db.Boolean, default=False)

    @staticmethod
    def reset_passwd(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.user_passwd = new_password
        db.session.add(user)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.user_id}).decode('utf-8')


    def generate_confirmation_token(self, expiration=3600):
        '''generate_confirmation_token() 方法生成一个令牌，有效期默认为一小时'''
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.user_id}).decode('utf-8')

    def confirm(self, token):
        '''confirm() 方法检验令牌，如果检验通过，就把用户模型中新添加的 confirmed 属性设为 True'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.user_id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def __repr__(self):
        return '<User %r>' % self.user_name

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