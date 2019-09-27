# -*- coding: utf-8 -*-


'''
Author : renwl
Date : 日期
Desc : 视图层
'''

from flask import render_template, request, current_app, redirect, jsonify, url_for
from . import main_bp
from flask_login import login_required, current_user
import pysnooper
from app.decorators import permission_required
from app.models import Permission, Post, User, Comment
from app import db
from .forms import SearchForm, CommentForm


@main_bp.route('/', methods=['GET', 'POST'])
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
        User.user_id).filter(
        Post.user_id == User.user_id).filter(Post.status == 1).order_by(
        Post.crtd_time.desc()).paginate(
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

    user = User.query.filter(User.user_id == userid).first()

    pagination = db.session.query(
        Post.post_id,
        Post.content,
        Post.body_html,
        Post.crtd_time,
        Post.title,
        User.user_name,
        User.user_id,
        User.location,
        User.about_me).filter(
        Post.user_id == User.user_id).filter(
        Post.user_id == userid).filter(Post.status == 1).order_by(
        Post.crtd_time.desc()).paginate(
        page,
        per_page=int(
            current_app.config['FLASKY_POSTS_PER_PAGE']),
        error_out=False)

    posts = pagination.items

    return render_template(
        'main/uplist.html',
        posts=posts,
        pagination=pagination,
        user=user,
        title_name='伯乐在线')
    # posts = db.session.query(Post.post_id, Post.content, Post.crtd_time,
    #                          Post.title, User.user_name, User.about_me, User.location, User.user_id).\
    #     filter(Post.user_id == User.user_id).\
    #     filter(Post.user_id == userid).order_by(Post.crtd_time.desc()).all()
    #
    # return render_template('main/uplist.html', posts=posts)


@main_bp.route('/getpost/<int:postid>', methods=['GET', 'POSt'])
@pysnooper.snoop()
def get_post(postid):
    '''博客详情展示页面,传入参数：博客id'''

    comment_form = CommentForm()

    from datetime import datetime

    if comment_form.validate_on_submit():
        comm = Comment(post_id=postid, comment_content=comment_form.comment_content.data, crtd_time=datetime.now(),
                       user_id=current_user.user_id)

        db.session.add(comm)
        db.session.commit()
        return redirect(url_for('main.get_post', postid=postid))

    post = db.session.query(
        Post.post_id,
        Post.content,
        Post.crtd_time,
        Post.body_html,
        Post.title,
        User.user_name,
        User.user_id,
        User.location,
        User.about_me).filter(
        Post.post_id == postid).filter(
        Post.user_id == User.user_id).first()
    user = User.query.filter(User.user_id == post.user_id).first()

    comments = db.session.query(Comment.post_id, Comment.comment_content, Comment.crtd_time, User.user_name).filter(
        User.user_id == Comment.user_id).filter_by(post_id=postid).all()

    # comments = Comment.query.filter_by(post_id=postid).all()

    return render_template('main/post.html', post=post, user=user, form=comment_form, comments=comments,
                           title_name='博客')


@main_bp.route('/search_post/', methods=['GET', 'POST'])
@pysnooper.snoop()
def search_post():
    '''搜索博客'''
    page = request.args.get('page', 1, type=int)
    searchform = SearchForm()
    key_word = searchform['key_word'].data

    if 1:  # searchform.validate_on_submit():
        pagination = db.session.query(
            Post.post_id,
            Post.content,
            Post.body_html,
            Post.crtd_time,
            Post.title,
            User.user_name,
            User.user_id).filter(
            Post.user_id == User.user_id) \
            .filter(Post.title.contains(key_word) | Post.body_html.contains(key_word)) \
            .order_by(
            Post.crtd_time.desc()).paginate(
            page,
            per_page=int(
                current_app.config['FLASKY_POSTS_PER_PAGE']),
            error_out=False)

        posts = pagination.items

        return render_template(
            'main/index.html',
            posts=posts,
            pagination=pagination,
            title_name='搜索结果')


@main_bp.route('/follow/<int:user_id>')
@pysnooper.snoop()
def follow(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if current_user.is_following(user):  # 判断是否关注
        current_user.unfollow(user)
        db.session.add(user)
        db.session.commit()
        return jsonify({'follow': '关注',
                        'fans': user.followers.count(),
                        'collects': user.followed.count(),
                        'location': user.location,
                        'about_me': user.about_me
                        })
    else:
        current_user.follow(user)
        db.session.add(user)
        db.session.commit()
        return jsonify({'follow': '取消关注',
                        'fans': user.followers.count(),
                        'collects': user.followed.count(),
                        'location': user.location,
                        'about_me': user.about_me
                        })


@main_bp.route('/unfollow/<int:user_id>')
def unfollow(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    current_user.unfollow(user)
    db.session.add(user)
    db.session.commit()
    return user
