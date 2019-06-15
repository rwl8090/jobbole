# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 表单
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from ..models import User
from wtforms import ValidationError


#表单类-登录
class LoginForm(FlaskForm):
    name = StringField("用户名：", validators=[DataRequired(message='名字忘填了')])
    passwd = PasswordField('密码：', validators=[DataRequired(message='请输入密码')])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    #user_name = StringField("用户名：", validators=[DataRequired(message='名字忘填了')])
    user_login_name = StringField("登录用户名：", validators=[DataRequired(message='名字忘填了')])
    user_passwd = PasswordField('密码：', validators=[DataRequired(),
                                                   EqualTo('user_passwd_confirm', message='密码必须一致'),
                                                   Length(8, message='密码不能低于8位')])
    user_passwd_confirm = PasswordField('确认密码：', validators=[DataRequired(message='确认密码')])
    submit = SubmitField('注册')

    # 表单类中定义了以 validate_
    # 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用
    def validate_user_login_name(self, field):
        if User.query.filter_by(user_login_name=field.data).first():
            raise ValidationError('用户名已存在')
