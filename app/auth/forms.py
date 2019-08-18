# -*- coding: utf-8 -*-
'''
Author : renwl
Date : 日期
Desc : 表单
'''
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from ..models import User
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField


# 表单类-登录
class LoginForm(FlaskForm):
    user_email = StringField("邮箱：", validators=[DataRequired(message='邮箱忘填了')])
    user_passwd = PasswordField(
        '密码：', validators=[
            DataRequired(
                message='请输入密码')])
    submit = SubmitField('登录')


class ChpasswdForm(FlaskForm):
    '''修改用户表单类'''
    old_user_passwd = PasswordField('旧密码：', validators=[DataRequired()])
    new_user_passwd = PasswordField(
        '新密码：', validators=[
            DataRequired(), EqualTo(
                'confirm_user_passwd', message='密码必须一致'), Length(
                8, message='密码不能低于8位')])
    confirm_user_passwd = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('修改')


class PasswdResetResponseForm(FlaskForm):
    '''用户密码重置表单类'''
    user_email = StringField(
        '邮箱：', validators=[
            DataRequired(), Length(
                1, 64), Email()])
    submit = SubmitField('密码重置')

    def validate_user_email(self, field):
        if not User.query.filter_by(user_email=field.data).first():
            raise ValidationError('邮箱未注册，请确认！')


class PasswdResetForm(FlaskForm):
    '''密码重置表单类'''
    new_user_passwd = PasswordField(
        '新密码：', validators=[
            DataRequired(), EqualTo(
                'confirm_user_passwd', message='密码必须一致'), Length(
                8, message='密码不能低于8位')])
    confirm_user_passwd = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('重置密码')


class RegisterForm(FlaskForm):
    user_name = StringField("用户名：", validators=[DataRequired(message='名字忘填了')])
    #user_login_name = StringField("登录用户名：", validators=[DataRequired(message='名字忘填了')])
    user_email = StringField(
        "注册邮箱：", validators=[
            DataRequired(), Length(
                1, 64), Email()])
    user_passwd = PasswordField(
        '密码：', validators=[
            DataRequired(), EqualTo(
                'user_passwd_confirm', message='密码必须一致'), Length(
                8, message='密码不能低于8位')])
    user_passwd_confirm = PasswordField(
        '确认密码：', validators=[
            DataRequired(
                message='确认密码')])
    submit = SubmitField('注册')

    # 表单类中定义了以 validate_
    # 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用
    # def validate_user_login_name(self, field):
    #     if User.query.filter_by(user_login_name=field.data).first():
    #         raise ValidationError('用户名已存在')
    def validate_user_email(self, field):
        if User.query.filter_by(user_email=field.data).first():
            raise ValidationError('邮箱已注册。')

    def validate_user_name(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('用户名已存在。')


class EditUserForm(FlaskForm):
    '''用户编辑表单'''
    user_name = StringField("用户名：")
    location = StringField("所在地：")
    about_me = TextAreaField("关于我：")
    submit = SubmitField("确认修改")


class EditPostForm(FlaskForm):
    '''编辑博客'''
    title = StringField("标题")
    content = PageDownField("内容", validators=[DataRequired()])
    submit = SubmitField("新增")
