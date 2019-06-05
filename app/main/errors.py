# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 错误验证
'''

from flask import render_template
from . import main_bp


# 在蓝本中编写错误处理程序稍有不同，如果使用 errorhandler 装饰器，那么只有蓝本中的
# 错误才能触发处理程序。要想注册应用全局的错误处理程序，必须使用 app_errorhandler
# 装饰器

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500