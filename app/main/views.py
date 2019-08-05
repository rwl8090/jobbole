# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template, request, current_app
from . import main_bp
from flask_login import login_required
from flask_mail import Message
from app import mail
import pysnooper
from app.decorators import admin_required, permission_required
from app.models import Permission, Post, User
from app import db


@main_bp.route('/', methods=['GET', 'POST'])
@pysnooper.snoop()
def index():
    page = request.args.get('page', 1, type=int)

    pagination = db.session.query(Post.post_id, Post.content, Post.crtd_time,
                    Post.title, User.user_name, User.user_id).\
                 filter(Post.user_id == User.user_id). \
                 order_by(Post.crtd_time.desc()). \
                 paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    # pagination = Post.query.order_by(Post.crtd_time.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    posts = pagination.items

    # posts = db.session.query(Post.post_id, Post.content, Post.crtd_time,
    #                          Post.title, User.user_name, User.user_id).\
    #     filter(Post.user_id == User.user_id).order_by(Post.crtd_time.desc()).all()
    return render_template('main/index.html', posts=posts, pagination=pagination, title_name='伯乐在线')


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


@main_bp.route('/uplist/<userid>')
def uplist(userid):
    '''主页用户点击展示个人博客页面等'''
    posts = db.session.query(Post.post_id, Post.content, Post.crtd_time,
                             Post.title, User.user_name, User.about_me, User.location, User.user_id).\
        filter(Post.user_id == User.user_id).\
        filter(Post.user_id == userid).order_by(Post.crtd_time.desc()).all()

    return render_template('main/uplist.html', posts=posts)








