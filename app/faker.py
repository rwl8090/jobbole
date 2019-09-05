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
from app.models import User, Post, Role
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


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


# users(10)
# posts(100)
# Role.insert_roles()