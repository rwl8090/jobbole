# -*- coding: utf-8 -*-


'''
Author : renwl
Date : 日期
Desc : 视图层
'''


from flask import render_template, request, current_app
from . import main_bp
from flask_login import login_required
import pysnooper
from app.decorators import permission_required
from app.models import Permission, Post, User
from app import db


@main_bp.route('/', methods=['GET', 'POST'])
@login_required
@pysnooper.snoop()
def index():
    page = request.args.get('page', 1, type=int)

    pagination = db.session.query(
        Post.post_id,
        Post.content,
        Post.body_html,
        Post.crtd_time,
        Post.title,
        User.user_name,
        User.user_id). filter(
        Post.user_id == User.user_id). order_by(
            Post.crtd_time.desc()). paginate(
                page,
                per_page=int(
                    current_app.config['FLASKY_POSTS_PER_PAGE']),
        error_out=False)

    # pagination = Post.query.order_by(Post.crtd_time.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)

    posts = pagination.items

    # posts = db.session.query(Post.post_id, Post.content, Post.crtd_time,
    #                          Post.title, User.user_name, User.user_id).\
    #     filter(Post.user_id == User.user_id).order_by(Post.crtd_time.desc()).all()
    return render_template(
        'main/index.html',
        posts=posts,
        pagination=pagination,
        title_name='伯乐在线')


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


@main_bp.route('/uplist/')
def uplist():
    '''主页用户点击展示个人博客页面等'''

    page = request.args.get('page', 1, type=int)
    userid = request.args.get('userid', type=int)

    pagination = db.session.query(
        Post.post_id,
        Post.content,
        Post.body_html,
        Post.crtd_time,
        Post.title,
        User.user_name,
        User.user_id,
        User.location,
        User.about_me). filter(
        Post.user_id == User.user_id). filter(
            Post.user_id == userid). order_by(
                Post.crtd_time.desc()). paginate(
                    page,
                    per_page=int(
                        current_app.config['FLASKY_POSTS_PER_PAGE']),
        error_out=False)

    posts = pagination.items

    return render_template(
        'main/uplist.html',
        posts=posts,
        pagination=pagination,
        title_name='伯乐在线')
    # posts = db.session.query(Post.post_id, Post.content, Post.crtd_time,
    #                          Post.title, User.user_name, User.about_me, User.location, User.user_id).\
    #     filter(Post.user_id == User.user_id).\
    #     filter(Post.user_id == userid).order_by(Post.crtd_time.desc()).all()
    #
    # return render_template('main/uplist.html', posts=posts)


@main_bp.route('/getpost/<int:postid>')
@pysnooper.snoop()
def get_post(postid):
    '''博客详情展示页面,传入参数：博客id'''

    post = db.session.query(
        Post.post_id,
        Post.content,
        Post.crtd_time,
        Post.body_html,
        Post.title,
        User.user_name,
        User.user_id,
        User.location,
        User.about_me). filter(
        Post.post_id == postid). filter(
            Post.user_id == User.user_id).first()

    return render_template('main/post.html', post=post, title_name='博客')


@main_bp.route()
@pysnooper.snoop()
def search_post():
    '''搜索博客'''

    pass