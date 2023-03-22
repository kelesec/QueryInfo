#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from flask import Blueprint

# 登陆验证
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 导出
from .admin import admin_bp
