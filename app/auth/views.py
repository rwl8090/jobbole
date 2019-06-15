# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''


from flask import render_template, session, redirect, url_for, flash, request
from . import auth_bp
from .forms import LoginForm, RegisterForm
from ..models import User
from DBHelper import DBHelper
from flask_login import login_user, login_required, logout_user
import pysnooper


@auth_bp.route('/login/', methods=['GET','POST'])
@pysnooper.snoop()
def login():
    '''用户登录'''
    loginform = LoginForm()
    if loginform.validate_on_submit():
        session['name'] = loginform.name.data
        user = User.query.filter_by(user_login_name=loginform.name.data).first()
        if user is not None and user.check_passwd_hash(loginform.passwd.data):
            ''' login_user() 函数的参数是要登录的用户，以及可选的“记住我”
布尔值，“记住我”也在表单中勾选。如果这个字段的值为 False ，关闭浏览器后用户会话
就过期了，所以下次用户访问时要重新登录。如果值为 True ，那么会在用户浏览器中写入
一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。cookie 默认记住一年，可以
使用可选的 REMEMBER_COOKIE_DURATION 配置选项更改这个值'''
            login_user(user, False)
            #next = request.args.get('next')
            #if next is None or not next.startswith('/'):
             #   next = url_for('main.index')
            return redirect(url_for('main.index'))
        else:
            flash('用户密码验证失败！')
        print(loginform.name.data, loginform.passwd.data)
        return redirect(url_for('.login'))
    return render_template('auth/login.html', form=loginform, title_name='登录')


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    '''注册用户'''
    rg_form = RegisterForm()  # 注册表单
    if rg_form.validate_on_submit():
        print('-------------------')
        rg_user = User(user_login_name=rg_form.user_login_name.data, user_passwd=rg_form.user_passwd.data)
        print(rg_form)
        helper = DBHelper()

        if helper.add_data(rg_user):
            flash('恭喜，用户注册成功，可以前往登录了！！')
        else:
            flash('糟糕，注册失败了，检查下输入用户名或密码！')
        return redirect(url_for('.register'))
    return render_template('auth/register.html', form=rg_form, title_name='用户注册')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('注销成功！！')
    return redirect(url_for('auth.login'))



