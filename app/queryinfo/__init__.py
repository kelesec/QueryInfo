#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from flask import Blueprint

queryinfo_bp = Blueprint("queryinfo", __name__, url_prefix="/query")
add_data_bp = Blueprint("add_data", __name__, url_prefix="/add")

from .queryinfo import queryinfo_bp
from .add_data import add_data_bp
