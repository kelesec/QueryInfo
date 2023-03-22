#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from app import mail
from flask_mail import Message
from flask import render_template


def send_email_reset_password(username, email, url_token):
    """发送密码重置邮件"""

    message_html = render_template(
        "email/reset.html",
        title="密码重置提醒",
        username=username,
        url=url_token
    )

    message = Message(
        subject="密码重置提醒",
        recipients=[email],
        html=message_html
    )

    mail.send(message)
