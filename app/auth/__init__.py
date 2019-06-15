# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='.templates/auth')


from . import views  # from . import <some-module> 句法表示相对导入