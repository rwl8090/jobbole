# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template
from . import main_bp
from flask_login import login_required
from flask_mail import Message
from app import mail
import pysnooper
from app.decorators import admin_required, permission_required
from app.models import Permission


@main_bp.route('/index', methods=['GET', 'POST'])
#@login_required
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('main.index'))
    return render_template('main/index.html', title_name='Index')


@main_bp.route('/send_email/')
@pysnooper.snoop()
def send_email():
    message = Message(subject=u'hello', recipients=['865178375@qq.com'], body=u'flask')
    try:
        print(message)
        mail.send(message)
        return '发送成功，请注意查收~'
    except Exception as e:
        print(e)
        return '发送失败'


@main_bp.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    return "For comment moderators!"


@main_bp.route('/roles')
def insert_roles():
    from app.models import Role
    Role.insert_roles()
    return 'hello'