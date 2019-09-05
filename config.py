# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdfjoejii-23---##t4ljlsdlgn'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = True # os.environ.get('MAIL_USE_TLS', 'true').lower() in  ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Flasky]'
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = os.environ.get('FLASKY_POSTS_PER_PAGE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # 259601nd01.qicp.vip
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://python:python_Pwd#012@192.168.18.159:3306/python'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jobbole.db')
config = {'development' : DevelopmentConfig}
