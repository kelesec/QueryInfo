#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from flask import render_template, request
from datetime import datetime
from . import add_data_bp
from .utils import *
from app import db
from app.admin.admin import login_required

# 当前年份
current_year = datetime.now().year


@add_data_bp.route("/", methods=["GET", "POST"], endpoint="index")
@login_required
def index():
    if request.method != "POST":
        return render_template("view/add_default.html", title="添加默认数据", current_year=current_year)

    forms = request.form

    if not forms.get("name"):
        return render_template("view/add_default.html",
                               title="添加默认数据", current_year=current_year, error="姓名字段必须添加")

    try:
        model = BaseTableModelFormat(forms).get_default_tale()
        db.session.add(model)
        db.session.commit()
    except:
        return render_template("view/add_default.html",
                               title="添加默认数据", current_year=current_year, error="添加失败")

    return render_template("view/add_default.html",
                           title="添加默认数据", current_year=current_year, succ="添加成功")


@add_data_bp.route("/edu", methods=["GET", "POST"], endpoint="add_edu")
@login_required
def add_edu():
    if request.method != "POST":
        return render_template("view/add_edu.html", title="添加学校信息", current_year=current_year)

    forms = request.form

    if not forms.get("name"):
        return render_template("view/add_edu.html",
                               title="添加学校信息", current_year=current_year, error="姓名字段必须添加")

    try:
        model = BaseTableModelFormat(forms).get_edu_table_model()
        db.session.add(model)
        db.session.commit()
    except:
        return render_template("view/add_edu.html",
                               title="添加学校信息", current_year=current_year, error="添加失败")

    return render_template("view/add_edu.html",
                           title="添加学校信息", current_year=current_year, succ="添加成功")


@add_data_bp.route("/pass", methods=["GET", "POST"], endpoint="add_pass")
@login_required
def add_pass():
    if request.method != "POST":
        return render_template("view/add_pass.html", title="添加密码信息")

    forms = request.form
    flag = True
    for v in forms.values():
        if v != '':
            flag = False
            break

    if flag:
        return render_template("view/add_pass.html", title="添加密码信息", error="至少需要添加一个字段")

    try:
        model = SocialUsersModelFormat(forms).get_social_user_model()
        db.session.add(model)
        db.session.commit()
    except:
        return render_template("view/add_pass.html", title="添加密码信息", error="添加失败")

    return render_template("view/add_pass.html", title="添加密码信息", succ="添加成功")


@add_data_bp.route("/weak_pwd", methods=["GET", "POST"], endpoint="add_weak_pwd")
@login_required
def add_weak_pwd():
    if request.method != "POST":
        return render_template("view/add_weak_pwd.html", title="添加常见设备弱口令")

    forms = request.form
    app_name = forms.get("app_name")
    username = forms.get("username")
    password = forms.get("password")
    official_website = forms.get("official_website")

    if app_name == '' or username=='' or password == '':
        return render_template("view/add_weak_pwd.html", title="添加常见设备弱口令", error="应用名|账户|密码必须添加")

    try:
        model = AppWeakPasswordModel(
            app_name=app_name,
            username=username,
            password=password,
            official_website=official_website)
        db.session.add(model)
        db.session.commit()
    except:
        return render_template("view/add_weak_pwd.html", title="添加常见设备弱口令", error="添加失败")

    return render_template("view/add_weak_pwd.html", title="添加常见设备弱口令", succ="添加成功")
