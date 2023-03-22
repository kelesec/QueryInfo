#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from wtforms import StringField, ValidationError, Form
from wtforms.validators import Email, length, EqualTo, DataRequired
from flask import session


def check_code(code):
    """验证码比较"""
    _code = session.get("checkcode")
    # print(_code.lower())
    # print(code.lower())
    if _code and _code.lower() == code.lower():
        return True


class InitForm(Form):
    """初始化表单，做初始值校验"""
    username = StringField(validators=[
        DataRequired(message="用户名不能为空"),
        length(min=4, max=20, message="用户名必须为 4~20 位之间")
    ])
    email = StringField(validators=[
        DataRequired(message="邮箱不能为空"),
        Email()
    ])
    password1 = StringField(validators=[
        DataRequired(message="密码不能为空"),
        length(min=6, max=20, message="密码必须在 6~20 位数之间"),
        EqualTo("password2", message="两次密码输入不一致")
    ])
    password2 = StringField()

    checkcode = StringField(validators=[
        DataRequired(message="请输入验证码"),
    ])

    def validate_checkcode(self, field):
        """验证码验证"""
        if not check_code(field.data):
            raise ValidationError("验证码错误")


class LoginForm(Form):
    """登陆表单验证"""
    username = StringField(validators=[DataRequired(message="用户名不能为空")])
    password = StringField(validators=[DataRequired(message="密码不能为空")])
    checkcode = StringField(validators=[DataRequired(message="验证码不能为空")])

    def validate_checkcode(self, field):
        """验证码验证"""
        if not check_code(field.data):
            raise ValidationError("验证码错误")


class ForgetForm(Form):
    """忘记密码表单验证"""
    email = StringField(validators=[
        DataRequired(message="邮箱不能为空"),
        Email()
    ])
    checkcode = StringField(validators=[
        DataRequired(message="验证码不能为空")
    ])

    def validate_checkcode(self, field):
        """验证码验证"""
        if not check_code(field.data):
            raise ValidationError("验证码错误")


class ResetForm(Form):
    password1 = StringField(validators=[
        DataRequired(message="密码不能为空"),
        length(min=6, max=20, message="密码必须在 6~20 位数之间"),
        EqualTo("password2", message="两次密码输入不一致")
    ])
    password2 = StringField()


class ModifyForm(Form):
    email = StringField(validators=[
        DataRequired(message="邮箱不能为空"),
        Email()
    ])
    password1 = StringField(validators=[
        DataRequired(message="密码不能为空"),
        length(min=6, max=20, message="密码必须在 6~20 位数之间"),
    ])
    password2 = StringField(validators=[
        DataRequired(message="密码不能为空"),
        length(min=6, max=20, message="密码必须在 6~20 位数之间"),
    ])
