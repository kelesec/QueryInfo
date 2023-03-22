#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from .import admin_bp
from flask import (
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
    abort,
    g,
    flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from string import digits, ascii_letters
from app.models.admin_models import *
from .forms import InitForm, LoginForm, ForgetForm, ResetForm, ModifyForm
from app import db
from datetime import datetime
from .email import send_email_reset_password
import random


def login_required(function):
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return function(*args, **kwargs)
        else:
            return redirect(url_for('admin.login'))
    return wrapper


def get_captcha(num):
    """获取 num 位数长度的验证码"""
    captcha_model = digits + ascii_letters
    return "".join(random.sample(captcha_model, num))


@admin_bp.route('/code', methods=["POST"])
def send_code():
    if request.method != 'POST':
        return jsonify({'code': 400, 'msg': '请求错误'})

    checkcode = get_captcha(4)
    session['checkcode'] = checkcode
    return jsonify({'code': 200, 'checkcode': checkcode})


@admin_bp.route('/init', methods=["GET", "POST"])
def init():
    """初始化，第一次使用时创建管理员"""
    # 检测是否已经存在用户
    users = UsersModel.query.all()
    if users:
        abort(404)

    if request.method != 'POST':
        return render_template('admin/init.html', title="创建管理员账户", subheading='QueryInfo社工查询系统')

    form = InitForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[0]
        return {'code': 400, 'msg': error}

    username = form.username.data
    email = form.email.data
    password = form.password1.data

    # 存入数据库
    user = UsersModel(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    # 清空 session
    session.clear()

    return jsonify({'code': 200, "msg": "创建成功"})


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登陆"""
    if request.method != 'POST':
        return render_template('admin/login.html', title='管理员登陆', subheading='QueryInfo社工查询系统')

    form = LoginForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[0]
        session.clear()
        return jsonify({'code': 400, 'msg': error})

    username = form.username.data
    password = form.password.data

    user = UsersModel.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session.clear()
        session['id'] = user.id
        return jsonify({"code": 200, "msg": "登陆成功"})
    else:
        session.clear()
        return jsonify({'code': 400, 'msg': '用户名或密码错误'})


@admin_bp.route('/logoff')
def logoff():
    session.clear()
    return redirect(url_for('admin.login'))


@admin_bp.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method != 'POST':
        return render_template('admin/forget.html', title="忘记密码", subheading='QueryInfo社工查询系统')

    form = ForgetForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[0]
        return jsonify({'code': 400, 'msg': error})

    email = form.email.data
    user = UsersModel.query.filter_by(email=email).first()

    if user:
        session.clear()
        token = get_captcha(52)
        user_token = TokenModel.query.filter_by(email=email).first()

        if user_token:
            # 防止验证码重复发送
            current_time = datetime.now()
            effect_time = current_time - user_token.update_time
            if effect_time.total_seconds() < 60.0:
                return jsonify({"code": 400, "msg": "请勿重复发送"})

            user_token.token = token
            user_token.is_lock = False  # 解除锁定
            db.session.commit()
        else:
            tm = TokenModel(email=email, token=token, is_lock=False)
            db.session.add(tm)
            db.session.commit()

        url_token = request.url_root + "admin/reset?token=%s&email=%s" % (token, email)
        try:
            send_email_reset_password(user.username, email, url_token=url_token)
            return jsonify({'code': 200, 'msg': '发送成功'})
        except:
            return jsonify({'code': 400, 'msg': '发送失败'})
    else:
        session.clear()
        return jsonify({"code": 400, "msg": "用户不存在"})


@admin_bp.route('/reset', methods=["GET", "POST"])
def reset():
    token = request.args.get("token")
    email = request.args.get("email")
    if not token or not email:
        abort(404)

    user_token = TokenModel.query.filter_by(email=email.strip()).first()
    if not (user_token and user_token.token == token):
        abort(404)

    if user_token.is_lock:
        abort(404)

    if not request.method == "POST":
        return render_template("admin/reset.html", title="重置密码", subheading="QueryInfo社工查询系统")

    # 判断 token 有效时间
    current_time = datetime.now()
    effect_time = current_time - user_token.update_time
    if effect_time.total_seconds() > 600.0:
        return jsonify({"code": 400, "msg": "Token已过期，请重新发送"})

    form = ResetForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[0]
        return jsonify({"code": 400, "msg": error})

    password = form.password1.data
    user = UsersModel.query.filter_by(email=email).first()
    if user:
        # 修改密码
        user.password = generate_password_hash(password)
        # 修改成功，锁定Token
        user_token.is_lock = True
        db.session.commit()
        session.clear()
    else:
        return jsonify({"code": 400, "msg": "用户不存在，修改失败"})

    return jsonify({"code": 200, "msg": "修改成功"})


@admin_bp.route("/modify", methods=["GET", "POST"])
def modify():
    # 判断是否登陆
    if not session.get('id'):
        return redirect(url_for('admin.login'))

    if not request.method == 'POST':
        return render_template('admin/modify.html', title='修改密码')

    form = ModifyForm(request.form)
    if not form.validate():
        error = list(form.errors.values())[0][0]
        flash(error)
        return render_template('admin/modify.html', title='修改密码')

    email = form.email.data
    password1 = form.password1.data
    password2 = form.password2.data

    try:
        user = UsersModel.query.get(session.get('id'))
        if not user:
            raise Exception()
        if not check_password_hash(user.password, password1):
            flash("原密码错误")
            return render_template('admin/modify.html', title='修改密码')

        user.email = email
        user.password = generate_password_hash(password2)
        db.session.commit()
        flash("修改成功")
    except:
        flash("修改失败")

    return render_template('admin/modify.html', title='修改密码')
