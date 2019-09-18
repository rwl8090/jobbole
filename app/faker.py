# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     faker
   Description :
   Author :       Ealine
   date：           2019-08-04 21:41
-------------------------------------------------
   Change Activity:  

-------------------------------------------------
"""
__author__ = 'Ealine'

from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from jobbole import db
from app.models import User, Post, Role, Follow, Comment


def users(count=100):
    faker = Faker(locale='zh_CN')
    i = 0
    while i < count:
        u = User(user_name=faker.user_name(),
                 user_email=faker.email(),
                 user_passwd='passwd',
                 confirmed=True,
                 location=faker.city(),
                 about_me=faker.text(),
                 member_since=faker.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def posts(count=100):
    faker = Faker(locale='zh_CN')
    user_count = User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(content=faker.text(),
                 title=faker.text()[1:15],
                 crtd_time=faker.date_time(),
                 user_id=u.user_id)
        db.session.add(p)
    db.session.commit()


def follow(count=100):
    user_count = User.query.count()

    for i in range(count):
        u1 = User.query.offset(randint(0, user_count - 1)).first()
        u2 = User.query.offset(randint(0, user_count - 1)).first()
        if u1.user_id != u2.user_id:
            f = Follow(follower_id=u1.user_id,
                       followed_id=u2.user_id)
            db.session.add(f)
    db.session.commit()


def comments(count=50):
    user_count = User.query.count()
    post_count = Post.query.count()
    faker = Faker(locale='zh_CN')
    for i in range(count):
        u1 = User.query.offset(randint(0, user_count - 1)).first()
        p1 = Post.query.offset(randint(0, post_count - 1)).first()


        comm = Comment(user_id=u1.user_id, post_id=p1.post_id, comment_content=faker.text())
        db.session.add(comm)
    db.session.commit()




# users(10)
# posts(100)
# Role.insert_roles()
