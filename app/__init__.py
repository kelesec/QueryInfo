#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from .config.settings import BASE_DIR


# 初始化
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app():
    # Create app
    app = Flask(__name__, instance_relative_config=True)

    # 加载配置文件
    try:
        CONFIG_FILE = BASE_DIR / 'app/config/settings.py'
        app.config.from_pyfile(CONFIG_FILE)
    except Exception:
        raise Exception("加载配置文件错误")

    # 绑定
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # 注册 admin_bp
    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    # 注册 query_bp
    from .queryinfo import queryinfo_bp
    app.register_blueprint(queryinfo_bp)

    from .queryinfo import add_data_bp
    app.register_blueprint(add_data_bp)

    return app
