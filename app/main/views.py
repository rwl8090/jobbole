# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template, session, redirect, url_for, flash
from . import main_bp
from .forms import LoginForm, RegisterForm
from ..models import User
from DBHelper import DBHelper


@main_bp.route('/', methods=['GET','POST'])
def index():
    # form = NameForm()
    # if form.validate_on_submit():
    #     return redirect(url_for('main.index'))
    return render_template('index.html', title_name='Index')


@main_bp.route('/login/', methods=['GET','POST'])
def loginform():
    '''用户登录'''
    loginform = LoginForm()
    if loginform.validate_on_submit():
        session['name'] = loginform.name.data
        print(loginform.name.data, loginform.passwd.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=loginform, title_name='登录')


@main_bp.route('/register/', methods=['GET', 'POST'])
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
    return render_template('register.html', form=rg_form, title_name='用户注册')


