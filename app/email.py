# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 邮件
'''

from app import mail
from flask_mail import Message
from flask import render_template
from threading import Thread
from jobbole import app
import pysnooper

@pysnooper.snoop()
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@pysnooper.snoop()
def send_email(to, subject, template, **kwargs):
    msg = Message(#app.config['MAIL_SUBJECT_PREFIX'] +
                  subject,
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[to])
    msg.body =  render_template(template + '.txt', **kwargs)
    #msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

