# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 描述内容
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


#表单类
class NameForm(FlaskForm):
    name = StringField("能告诉我你的名字吗？", validators=[DataRequired(message='名字忘填了。。。')])
    submit = SubmitField('告知一下！')


    