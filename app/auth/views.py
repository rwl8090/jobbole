# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''


from flask import render_template, session, redirect, url_for, flash, request
from . import auth_bp
from .forms import LoginForm, RegisterForm, ChpasswdForm, PasswdResetForm, PasswdResetResponseForm
from ..models import User
from flask_login import login_user, login_required, logout_user, current_user
import pysnooper
from app import db
from ..email import send_email


@auth_bp.route('/login/', methods=['GET','POST'])
@pysnooper.snoop()
def login():
    '''用户登录'''
    loginform = LoginForm()
    if loginform.validate_on_submit():
        session['user_email'] = loginform.user_email.data
        user = User.query.filter_by(user_email=loginform.user_email.data).first()
        if user is not None and user.check_passwd_hash(loginform.user_passwd.data):
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
        print(loginform.user_email.data, loginform.user_passwd.data)
        return redirect(url_for('.login'))
    return render_template('auth/login.html', form=loginform, title_name='登录')


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    '''注册用户'''
    rg_form = RegisterForm()  # 注册表单

    if rg_form.validate_on_submit():
        rg_user = User(user_name=rg_form.user_name.data, \
                       user_email=rg_form.user_email.data, \
                       user_passwd=rg_form.user_passwd.data)

        try:
            db.session.add(rg_user)
            db.session.commit()
            token = rg_user.generate_confirmation_token()
            send_email(rg_user.user_email, 'Confirm Your Account', 'email/confirm', user=rg_user, token=token)
            flash('恭喜，用户注册成功，请前往邮箱确认！！')
        except Exception as e:
            flash('糟糕，注册失败了，检查下输入用户名或密码！', e)
        return redirect(url_for('.register'))
    return render_template('auth/register.html', form=rg_form, title_name='用户注册')


@auth_bp.route('/confirm/<token>/')
@login_required
@pysnooper.snoop()
def confirm(token):
    '''需登录验证'''
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('必须登录才能验证账户！')
    else:
        flash('验证连接已失效！')
    return redirect(url_for('main.index'))


@auth_bp.route('/ulgconfirm/<token>/')
@pysnooper.snoop()
def ulgconfirm(token):
    '''非登录验证'''

    uid = User.ulgconfirm(token=token)
    if uid:
        user = User.query.filter_by(user_id=uid).first()
        if user.confirmed:
            flash('该用户已确认，请勿重新确认！')
            return redirect(url_for('auth.login'))
        else:
            user.confirmed=True
            db.session.add(user)
            db.session.commit()
            flash('用户已确认，请登录')
            return redirect(url_for('auth.login'))
    else:
        flash('url无效，请重新确认！')
        return redirect(url_for('auth.login'))



@auth_bp.route('/logout')
@login_required
def logout():
    '''用户注销'''
    logout_user()
    flash('注销成功！！')
    return redirect(url_for('auth.login'))


@auth_bp.route('/chpasswd/', methods=['GET', 'POST'])
@login_required
@pysnooper.snoop()
def chpasswd():
    '''登录用户修改密码'''
    passwd_form = ChpasswdForm()
    if passwd_form.validate_on_submit():
       if current_user.check_passwd_hash(passwd_form.old_user_passwd.data): # 校对原始密码
           current_user.user_passwd = passwd_form.new_user_passwd.data
           db.session.add(current_user)
           db.session.commit()
           flash('密码已重置，请重新登录')
           logout_user()
           return redirect(url_for('auth.login'))
       else:
           flash('原始密码错误！！')
    return render_template('auth/chpasswd.html', form=passwd_form, title_name='修改密码')


@auth_bp.route('/forget_passwd/', methods=['GET', 'POST'])
@pysnooper.snoop()
def forget_passwd():
    '''忘记密码'''
    form = PasswdResetResponseForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data.lower()).first()
        token = user.generate_reset_token()
        try:
            send_email(user.user_email, '重置密码', 'email/reset_passwd', user=user, token=token)
            flash('重置密码邮件已发送，请注意查收确认！')
        except:
            flash('邮件发送失败了！！！')
        return redirect(url_for('.forget_passwd'))
    return render_template('auth/forget_passwd.html', form=form, title_name='忘记密码')


@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswdResetForm()
    if form.validate_on_submit():
        if User.reset_passwd(token, form.new_user_passwd.data):
            db.session.commit()
            flash('你的密码已重置，请重新登录！')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_passwd.html', form=form, title_name='重置密码')