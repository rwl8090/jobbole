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
from datetime import datetime


# class AnonymousUser(AnonymousUserMixin):
#     # confirmed = False
#     @property
#     def confirmed(self):
#         return False

# 关注用户 FOLLOW 1
# 在他人的文章中发表评论 COMMENT 2
# 写文章 WRITE 4
# 管理他人发表的评论 MODERATE 8
# 管理员权限 ADMIN 16

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


# 数据库类
class Role(db.Model):
    __tablename__ = 'role'  # 指定表名
    role_id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    role_name = db.Column(db.String(50), unique=True, comment='角色名称')
    default = db.Column(db.Boolean, default=False, index=True)
    permission = db.Column(db.Integer)

    user = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permission is None:
            self.permission = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    def has_permission(self, perm):
        '''查询是否具有此权限  '''
        return self.permission & perm == perm

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permission += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permission -= perm

    def reset_permissions(self):
        self.permission = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.role_name == default_role)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, comment='用户ID')
    user_name = db.Column(db.String(50), unique=True, comment='用户名')
    user_email = db.Column(db.String(20), unique=True, comment='邮箱')
    user_mbl_nm = db.Column(db.String(20), unique=True, comment='用户电话')
    user_passwd_hash = db.Column(db.String(255), comment='用户密码')
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))
    confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    def ping(self):
        '''更新用户最后登录时间'''
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()





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

    @staticmethod
    def ulgconfirm(token):
        '''无登录验证'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        return data.get('confirm')

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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.user_email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(role_name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


@manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
