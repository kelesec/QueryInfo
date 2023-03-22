#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from app import db
from datetime import datetime


class BaseModel(db.Model):
    """基类模板"""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class UsersModel(BaseModel):
    """管理员用户模型"""
    __tablename__ = "users"

    username  = db.Column(db.String(128), unique=True, nullable=False)
    password  = db.Column(db.String(128), nullable=False)
    email     = db.Column(db.String(128), unique=True, nullable=False)


class TokenModel(BaseModel):
    """临时 token"""
    __tablename__ = "user_token"

    email = db.Column(db.String(128), unique=True, nullable=False)
    token = db.Column(db.String(128), nullable=False)
    is_lock = db.Column(db.Boolean, default=True, nullable=False)
