#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from .admin_models import BaseModel
from .admin_models import db


class BaseTableModel(BaseModel):
    """基类模型"""
    __abstract__ = True

    name            = db.Column(db.String(128), nullable=False, index=True, comment="姓名")
    sex             = db.Column(db.Boolean, default=True, nullable=False, comment="性别")  # true -> 男
    birthday        = db.Column(db.Date, nullable=True, comment="出生日期")
    telephone       = db.Column(db.String(20), nullable=True, index=True, comment="电话")
    email           = db.Column(db.String(128), nullable=True, index=True, comment="邮箱")
    id_card         = db.Column(db.String(20), nullable=True, index=True, comment="身份证")
    address         = db.Column(db.String(128), nullable=True, comment="家庭住址")
    occupation      = db.Column(db.String(128), nullable=True, comment="职业")
    workplace         = db.Column(db.String(128), nullable=True, index=True, comment="工作单位")
    education       = db.Column(db.String(128), nullable=True, comment="学历")
    common_password = db.Column(db.String(128), nullable=True, comment="常用密码")
    other           = db.Column(db.Text, nullable=True, comment="其它")

    def get_info(self):
        """获得详细信息"""
        sex = "男" if self.sex else "女"
        return {
            "姓名": self.name,
            "性别": sex,
            "出生日期": self.birthday,
            "电话": self.telephone,
            "邮箱": self.email,
            "身份证号": self.id_card,
            "家庭住址": self.address,
            "职业": self.occupation,
            "工作单位": self.workplace,
            "学历": self.education,
            "常用密码": self.common_password,
            "其他信息": self.other
        }

    def get_hd(self):
        """获取每个字段对应的解释信息"""
        sex = "男" if self.sex else "女"
        return {
            'id': self.id,
            'data': {
                "姓名": self.name,
                "性别": sex,
                "出生日期": self.birthday,
                "电话": self.telephone,
                "邮箱": self.email,
                "身份证号": self.id_card,
                "家庭住址": self.address,
                "职业": self.occupation,
                "工作单位": self.workplace,
                "学历": self.education,
                "常用密码": self.common_password,
                "其他信息": self.other
            }
        }


class DefaultTableModel(BaseTableModel):
    """默认表"""
    __tablename__ = "default_table"


class EduTableModel(BaseTableModel):
    """学校信息"""
    __tablename__ = 'edu_table'

    stu_card = db.Column(db.String(128), nullable=True, index=True, comment="学号")
    job_card = db.Column(db.String(128), nullable=True, index=True, comment="工号")

    def get_info(self):
        info = super(EduTableModel, self).get_info()
        info['学号'] = self.stu_card
        info['工号'] = self.job_card
        return info

    def get_hd(self):
        hd = super(EduTableModel, self).get_hd()
        hd['data']['学号'] = self.stu_card
        hd['data']['工号'] = self.job_card
        return hd


class AppWeakPasswordModel(BaseModel):
    """常用设备弱口令"""
    __tablename__ = "app_weak_password"

    app_name         = db.Column(db.String(128), nullable=False, index=True, comment="应用")
    username         = db.Column(db.String(128), nullable=False, comment="账户")
    password         = db.Column(db.String(128), nullable=False, comment="密码")
    official_website = db.Column(db.String(128), nullable=True, index=True, comment="官网")

    def get_hd(self):
        return {
            "设备名": self.app_name,
            "用户名": self.username,
            "密码": self.password,
            "官网": self.official_website
        }


class SocialUsersModel(BaseModel):
    """收录账户和密码"""
    __tablename__ = "social_users_table"

    uid         = db.Column(db.String(128), nullable=True, comment='用户ID')
    username    = db.Column(db.String(128), nullable=True, comment='用户名')
    password    = db.Column(db.String(128), nullable=True, comment='密码')
    encry_type  = db.Column(db.String(128), nullable=True, default='明文', comment='加密类型')
    salt        = db.Column(db.String(128), nullable=True, comment='盐值')
    email       = db.Column(db.String(128), nullable=True, comment='邮箱')
    qq          = db.Column(db.String(128), nullable=True, comment='QQ号')
    wechat      = db.Column(db.String(128), nullable=True, comment='微信')
    weibo       = db.Column(db.String(128), nullable=True, comment='微博')
    telephone   = db.Column(db.String(128), nullable=True, comment='电话号码')
    category    = db.Column(db.String(128), nullable=True, default='未分类', comment='分类')

    def get_info(self):
        return {
            "用户ID": self.uid,
            "用户名": self.username,
            "密码": self.password,
            "加密类型": self.encry_type,
            "盐值": self.salt,
            "邮箱": self.email,
            "QQ号": self.qq,
            "微信": self.wechat,
            "微博": self.weibo,
            "电话号码": self.telephone,
            "分类": self.category
        }

    def get_hd(self):
        return {
            'id': self.id,
            'data': {
                "用户ID": self.uid,
                "用户名": self.username,
                "密码": self.password,
                "加密类型": self.encry_type,
                "盐值": self.salt,
                "邮箱": self.email,
                "QQ号": self.qq,
                "微信": self.wechat,
                "微博": self.weibo,
                "电话号码": self.telephone,
                "分类": self.category
            }
        }
