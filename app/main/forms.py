# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 表单
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# 表单类-主页搜索
class SearchForm(FlaskForm):
    key_word = StringField("搜索：", validators=[DataRequired(message='没填入任何内容')])
    submit = SubmitField('搜索')


