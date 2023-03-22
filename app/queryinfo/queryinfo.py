#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from .import queryinfo_bp
from app.admin.admin import login_required

from flask import (
    render_template,
    request
)
from app.models.data_model import *


@queryinfo_bp.route("/", methods=["GET", "POST"], endpoint='index')
@login_required
def index():
    return render_template('index.html')


@queryinfo_bp.route("/about", methods=['GET', 'POST'], endpoint='about')
@login_required
def about():
    return render_template('view/index.html')


@queryinfo_bp.route("/default/info/<int:uid>", endpoint='search_one')
@login_required
def search_one(uid):
    data = DefaultTableModel.query.filter_by(id=uid).first()
    # print(data.get_info())
    if data:
        return render_template('view/info.html', data=data.get_info())
    else:
        return render_template('view/info.html')


def get_params(values: str):
    """拆分参数"""
    values = values.split('&&')
    values = [i.strip().replace(' ', '') for i in values]
    dic = {}
    for i in values:
        t = i.split('=')
        dic[t[0]] = t[1].replace('"', '').replace("'", "")
    return dic


def default_sql_filter(_dic: dict, model: BaseModel):
    """组合语句: name tel email id_card company"""
    filters = []
    if 'name' in _dic:
        filters.append(model.name.like(f"%{_dic.get('name')}%"))
    if 'tel' in _dic:
        filters.append((model.telephone.like(f"%{_dic.get('tel')}%")))
    if 'email' in _dic:
        filters.append((model.email.like(f"%{_dic.get('email')}%")))
    if 'id_card' in _dic:
        filters.append((model.id_card.like(f"%{_dic.get('id_card')}%")))
    if 'workplace' in _dic:
        filters.append(model.workplace.like("%{}%".format(_dic.get('workplace'))))

    return filters


@queryinfo_bp.route("/default", methods=["GET", "POST"], endpoint='search')
@login_required
def search():
    if request.method != 'POST':
        return render_template('view/default_search.html')

    _search = request.form.get('search')
    if not _search:
        return render_template('view/default_search.html')

    try:
        params = get_params(_search)
    except:
        return render_template('view/default_search.html', notice="语法错误")

    filters = default_sql_filter(params, DefaultTableModel)
    if not filters:
        return render_template('view/default_search.html', notice="语法错误")

    result = DefaultTableModel.query.filter(*filters).all()
    if not result:
        return render_template('view/default_search.html', notice="未收录该数据")

    # 整理数据
    datas = []
    for i in result:
        datas.append(i.get_hd())
    headers = datas[0]['data'].keys()

    return render_template('view/default_search.html', datas=datas, headers=headers)


def edu_filter(_dic, model: BaseTableModel):
    """组合SQL条件"""
    filters = default_sql_filter(_dic, model)
    if 'stu_card' in _dic:
        filters.append(model.stu_card == _dic.get('stu_card'))
    if 'job_card' in _dic:
        filters.append(model.job_card == _dic.get('job_card'))

    return filters


@queryinfo_bp.route("/edu/info/<int:uid>", endpoint="search_one_edu")
@login_required
def search_one_edu(uid):
    data = EduTableModel.query.filter_by(id=uid).first()
    if data:
        return render_template('view/info.html', data=data.get_info())
    else:
        return render_template('view/info.html')


@queryinfo_bp.route("/edu", methods=['GET', 'POST'], endpoint='edu_search')
@login_required
def edu_search():
    if request.method != 'POST':
        return render_template('view/edu_search.html')

    _search = request.form.get('search')
    if not _search:
        return render_template('view/edu_search.html')

    try:
        params = get_params(_search)
    except:
        return render_template('view/edu_search.html', notice="语法错误")

    filters = edu_filter(params, EduTableModel)
    if not filters:
        return render_template('view/edu_search.html', notice="语法错误")

    results = EduTableModel.query.filter(*filters).all()
    if not results:
        return render_template('view/edu_search.html', notice='未收录该数据')

    # 整理数据
    datas = []
    for i in results:
        datas.append(i.get_hd())
    headers = datas[0]['data'].keys()
    # print(datas)

    return render_template('view/edu_search.html', headers=headers, datas=datas)


@queryinfo_bp.route('/getpass/info/<int:uid>', endpoint='search_one_pwd')
@login_required
def search_one_pwd(uid):
    data = SocialUsersModel.query.filter_by(id=uid).first()
    if data:
        return render_template('view/info.html', data=data.get_info())
    else:
        return render_template('view/info.html')


def pwd_filter(_dic):
    """整理查询语句"""
    filters = []
    if 'uid' in _dic:
        filters.append(SocialUsersModel.uid == _dic.get('uid'))
    if 'name' in _dic:
        filters.append(SocialUsersModel.username.like(f"%{_dic.get('name')}%"))
    if 'email' in _dic:
        filters.append(SocialUsersModel.email.like(f"%{_dic.get('email')}%"))
    if 'qq' in _dic:
        filters.append(SocialUsersModel.qq == _dic.get('qq'))
    if 'wechat' in _dic:
        filters.append(SocialUsersModel.wechat == _dic.get('wechat'))
    if 'weibo' in _dic:
        filters.append(SocialUsersModel.weibo == _dic.get('weibo'))
    if 'tel' in _dic:
        filters.append(SocialUsersModel.telephone == _dic.get('tel'))
    if 'category' in _dic:
        filters.append(SocialUsersModel.category.like(f"%{_dic.get('category')}%"))

    return filters


@queryinfo_bp.route('/getpass', endpoint='search_pwd', methods=['GET', 'POST'])
@login_required
def search_pwd():
    if request.method != 'POST':
        return render_template('view/getpass.html')

    _search = request.form.get('search')
    if not _search:
        return render_template('view/getpass.html')

    try:
        params = get_params(_search)
    except:
        return render_template('view/getpass.html', notice="语法错误")

    filters = pwd_filter(params)
    if not filters:
        return render_template('view/getpass.html', notice="语法错误")

    results = SocialUsersModel.query.filter(*filters).all()
    if not results:
        return render_template('view/getpass.html', notice='未收录该数据')

    # 整理数据
    datas = []
    for i in results:
        datas.append(i.get_hd())
    headers = datas[0]['data'].keys()
    # print(datas)

    return render_template('view/getpass.html', headers=headers, datas=datas)


@queryinfo_bp.route("/app_weak", methods=['GET', 'POST'], endpoint='app_weak_pwd')
@login_required
def app_weak_pwd():
    if request.method != 'POST':
        return render_template('view/app_weak_password.html')

    _search = request.form.get('search')
    if not _search:
        return render_template('view/app_weak_password.html')

    datas = []

    if _search == 'all':
        results = AppWeakPasswordModel.query.all()
    else:
        results = AppWeakPasswordModel.query.filter(AppWeakPasswordModel.app_name.like(f'%{_search}%')).all()

    if not results:
        return render_template('view/app_weak_password.html', notice="未收录该数据")
    for i in results:
        datas.append(i.get_hd())

    headers = datas[0].keys()
    return render_template('view/app_weak_password.html', datas=datas, headers=headers)
