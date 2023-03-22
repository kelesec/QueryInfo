#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: kele

from flask import render_template, redirect, url_for, g, session
from app import create_app
from app.models.admin_models import UsersModel


app = create_app()


@app.before_request
def before_req():
    id = session.get('id')
    if id:
        try:
            user = UsersModel.query.get(id)
            setattr(g, 'user', user)
        except:
            setattr(g, 'user', None)


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {'user': None}


@app.route("/")
def index():
    users = UsersModel.query.all()
    if not users:
        return redirect(url_for("admin.init"))

    return redirect(url_for('queryinfo.index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
