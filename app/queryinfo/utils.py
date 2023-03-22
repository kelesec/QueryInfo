#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from ..models.data_model import *
from datetime import date


class BaseTableModelFormat(object):
    """获取BaseTableModel类型"""

    def __init__(self, forms):
        self.name = forms.get("name")
        self.sex = True if forms.get("sex") == "1" else False
        year = int(forms.get("birth-year"))
        month = int(forms.get("birth-month"))
        day = int(forms.get("birth-day"))
        self.birthday = date(year, month, day)
        self.telephone = forms.get("telephone")
        self.email = forms.get("email")
        self.id_card = forms.get("id_card")
        self.address = forms.get("address")
        self.occupation = forms.get("occupation")
        self.workplace = forms.get("workplace")
        self.education = forms.get("education")
        self.common_password = forms.get("common_password")
        self.other = forms.get("other")
        self.stu_card = forms.get("stu_card")
        self.job_card = forms.get("job_card")

    def get_default_tale(self):
        return DefaultTableModel(
            name=self.name,
            sex=self.sex,
            birthday=self.birthday,
            telephone=self.telephone,
            email=self.email,
            id_card=self.id_card,
            address=self.address,
            occupation=self.occupation,
            workplace=self.workplace,
            education=self.education,
            common_password=self.common_password,
            other=self.other,
        )

    def get_edu_table_model(self):
        return EduTableModel(
            name=self.name,
            sex=self.sex,
            birthday=self.birthday,
            telephone=self.telephone,
            email=self.email,
            id_card=self.id_card,
            address=self.address,
            occupation=self.occupation,
            workplace=self.workplace,
            education=self.education,
            common_password=self.common_password,
            other=self.other,
            stu_card=self.stu_card,
            job_card=self.job_card
        )


class SocialUsersModelFormat(object):
    """获取SocialUsersModel类型"""

    def __init__(self, forms):
        self.uid = forms.get("uid"),
        self.username = forms.get("username"),
        self.password = forms.get("password"),
        self.encry_type = forms.get("encry_type"),
        self.salt = forms.get("salt"),
        self.email = forms.get("email"),
        self.qq = forms.get("qq"),
        self.wechat = forms.get("wechat"),
        self.weibo = forms.get("weibo"),
        self.telephone = forms.get("telephone"),
        self.category = forms.get("category"),

    def get_social_user_model(self):
        return SocialUsersModel(
            uid=self.uid,
            username=self.username,
            password=self.password,
            encry_type=self.encry_type,
            salt=self.salt,
            email=self.email,
            qq=self.qq,
            wechat=self.wechat,
            weibo=self.weibo,
            telephone=self.telephone,
            category=self.category,
        )
