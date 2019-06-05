# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''

from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='.templates')
'''应用的路由保存在包里的 app/main/views.py 模块中，而错误处理程序保存在 app/main/
errors.py 模块中。导入这两个模块就能把路由和错误处理程序与蓝本关联起来。注意，这
些模块在 app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，因为在 app/
main/views.py 和 app/main/errors.py 中还要导入 main 蓝本，所以除非循环引用出现在定义
main 之后，否则会致使导入出错'''
from . import views, errors  # from . import <some-module> 句法表示相对导入