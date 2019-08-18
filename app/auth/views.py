# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''


from flask import render_template, session, redirect, url_for, flash, request
from . import auth_bp
from .forms import LoginForm, RegisterForm, ChpasswdForm, PasswdResetForm, PasswdResetResponseForm, EditUserForm, EditPostForm
from ..models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
import pysnooper
from app import db
from ..email import send_email
from datetime import datetime


@auth_bp.route('/login/', methods=['GET', 'POST'])
@pysnooper.snoop()
def login():
    '''用户登录'''

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    loginform = LoginForm()
    if loginform.validate_on_submit():
        session['user_email'] = loginform.user_email.data
        user = User.query.filter_by(
            user_email=loginform.user_email.data).first()
        if user is not None and user.check_passwd_hash(
                loginform.user_passwd.data):
            ''' login_user() 函数的参数是要登录的用户，以及可选的“记住我”
布尔值，“记住我”也在表单中勾选。如果这个字段的值为 False ，关闭浏览器后用户会话
就过期了，所以下次用户访问时要重新登录。如果值为 True ，那么会在用户浏览器中写入
一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。cookie 默认记住一年，可以
使用可选的 REMEMBER_COOKIE_DURATION 配置选项更改这个值'''
            login_user(user, False)
            # return redirect(url_for('main.index'))
            return redirect(
                url_for(
                    'auth.user',
                    username=current_user.user_name))
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
        rg_user = User(user_name=rg_form.user_name.data,
                       user_email=rg_form.user_email.data,
                       user_passwd=rg_form.user_passwd.data)

        try:
            db.session.add(rg_user)
            db.session.commit()
            token = rg_user.generate_confirmation_token()
            send_email(
                rg_user.user_email,
                'Confirm Your Account',
                'email/confirm',
                user=rg_user,
                token=token)
            flash('恭喜，用户注册成功，请前往邮箱确认！！')
        except Exception as e:
            flash('糟糕，注册失败了，检查下输入用户名或密码！', e)
        return redirect(url_for('.register'))
    return render_template(
        'auth/register.html',
        form=rg_form,
        title_name='用户注册')


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
            user.confirmed = True
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
        if current_user.check_passwd_hash(
                passwd_form.old_user_passwd.data):  # 校对原始密码
            current_user.user_passwd = passwd_form.new_user_passwd.data
            db.session.add(current_user)
            db.session.commit()
            flash('密码已重置，请重新登录')
            logout_user()
            return redirect(url_for('auth.login'))
        else:
            flash('原始密码错误！！')
    return render_template(
        'auth/chpasswd.html',
        form=passwd_form,
        title_name='修改密码')



@auth_bp.route('/forget_passwd/', methods=['GET', 'POST'])
@pysnooper.snoop()
def forget_passwd():
    '''忘记密码'''
    form = PasswdResetResponseForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            user_email=form.user_email.data.lower()).first()
        token = user.generate_reset_token()
        try:
            send_email(
                user.user_email,
                '重置密码',
                'email/reset_passwd',
                user=user,
                token=token)
            flash('重置密码邮件已发送，请注意查收确认！')
        except BaseException:
            flash('邮件发送失败了！！！')
        return redirect(url_for('.forget_passwd'))
    return render_template(
        'auth/forget_passwd.html',
        form=form,
        title_name='忘记密码')


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
    return render_template(
        'auth/reset_passwd.html',
        form=form,
        title_name='重置密码')


@auth_bp.before_app_request
@pysnooper.snoop()
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            r = redirect(url_for('auth.unconfirmed'))
            return r


@auth_bp.route('/user/<username>')
@login_required
@pysnooper.snoop()
def user(username):
    user = User.query.filter_by(user_name=username).first_or_404()
    if user == current_user:  # 判断当前登录的用户是否为链接选择的用户
        return render_template('auth/user.html', user=user)
    return '链接错误。。。'


@auth_bp.route('/unconfirmed/')
def unconfirmed():
    return '用户未认证，请重新认证！！！'


@auth_bp.route('/edit_profile/', methods=['GET', 'POST'])
@pysnooper.snoop()
def edit_profile():
    edituserform = EditUserForm()
    if edituserform.validate_on_submit():
        current_user.user_name = edituserform.user_name.data
        current_user.location = edituserform.location.data
        current_user.about_me = edituserform.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('您的资料已更新！！！')
        return redirect(url_for('.user', username=current_user.user_name))
    edituserform.user_name.data = current_user.user_name
    edituserform.location.data = current_user.location
    edituserform.about_me.data = current_user.about_me
    return render_template(
        'auth/edit_profile.html',
        form=edituserform,
        title='用户编辑')


@auth_bp.route('/add_post/', methods=['GET', 'POST'])
@login_required
@pysnooper.snoop()
def add_post():
    editpostform = EditPostForm()
    if editpostform.validate_on_submit():
        post = Post(user_id=current_user.user_id,
                    title=editpostform.title.data,
                    content=editpostform.content.data,
                    crtd_time=datetime.now(),
                    last_edit_time=datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('增加博客成功！！')
        return redirect(url_for('auth.add_post'))
    return render_template(
        'auth/addpost.html',
        form=editpostform,
        title='新增博客')


@auth_bp.route('/list_post/', methods=['GET', 'POST'])
@login_required
@pysnooper.snoop()
def list_post():
    '''查看用户下所有的博客'''
    posts = Post.query.filter_by(user_id=current_user.user_id).all()

    return render_template('auth/listpost.html', posts=posts, title='我的博客')


@auth_bp.route('/editpost', methods=['GET', 'POST'])
@login_required
@pysnooper.snoop()
def editpost():
    '''修改博客'''
    postid = request.args.get('postid', type=int)
    editpostform = EditPostForm()
    post = Post.query.filter_by(post_id=postid).first()
    if editpostform.validate_on_submit():
        post.update({'title': editpostform.title.data,
                    'content': editpostform.content.data,
                    'last_edit_time' : datetime.now()})

        db.session.add(post)
        db.session.commit()
        flash('增加博客成功！！')
        return redirect(url_for('auth.list_post'))

    editpostform.title.data = post.title
    editpostform.content.data = post.content
    return render_template(
        'auth/addpost.html',
        form=editpostform,
        title='修改博客')




