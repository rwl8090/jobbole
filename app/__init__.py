# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator
from flask_login import LoginManager

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# nav = Nav()
# @nav.navigation()
# def mynavbar():
#     return Navbar(
#         'mysite',
#         View('Home', 'index'),
#     )
#
# nav=Nav()
# nav.register_element('top',Navbar(u'Flask入门',
#                                     View(u'主页','home'),
#                                     View(u'关于','about'),
#                                     Subgroup(u'项目',
#                                              View(u'项目一','about'),
#                                              Separator(),
#                                              View(u'项目二', 'service'),
#                                     ),
# ))

topbar = Navbar(u'伯乐在线',
                    View('主页', 'main.index'),
                    View('内容', 'main.index'),
                Subgroup(u'项目',
                         View(u'项目一', 'main.index'),
                         Separator(),
                         View(u'项目二', 'main.index'),
                         ),
                Subgroup(u'项目',
                         View(u'项目一', 'main.index'),
                         Separator(),
                         View(u'项目二', 'main.index'),
                         ),

                    )

nav = Nav()
nav.register_element('top', topbar)

manager = LoginManager()
# LoginManager 对象的 login_view 属性用于设置登录页面的端点。匿名用户尝试访问受保护的页面时，Flask-Login 将重定向到登录页面
manager.login_view = 'auth.login'
manager.login_message = u"没有权限访问，请登录。"   # 定制无访问权限时提示消息

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 初始化插件
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    nav.init_app(app)
    manager.init_app(app)


    from .main import main_bp as main_blueprint
    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(main_blueprint) #, url_prefix='/')  # 注册蓝本
    app.register_blueprint(auth_blueprint)  # 注册蓝本

    return app








