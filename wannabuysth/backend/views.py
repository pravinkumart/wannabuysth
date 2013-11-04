# -*- coding: UTF-8 -*-
import logging
from flask import Blueprint, render_template, abort, g, request
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import AdminUser
from datetime import datetime
from utils import add_error, add_success

admin = Blueprint('backend', __name__, template_folder='templates', url_prefix='/admin')

@admin.route("/init", methods=["GET", "POST"])
def admin_init():
    '''
    @note: 初始化第一个管理员帐号
    '''
    users = g.db.query(AdminUser)
    if users.count() == 0:
        rec = AdminUser(name='admin', password='admin', mobile='15982150122')
        g.db.add(rec)
        g.db.commit()
    return redirect('/admin/login')

@admin.route("/", methods=["GET", "POST"])
@admin.route("/index", methods=["GET", "POST"])
def admin_index():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        return render_template("admin/index.html", **locals())

@admin.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if not username or not password:
            add_error(u'手机号或密码不能为空')
        else:
            users = g.db.query(AdminUser).filter(AdminUser.mobile == username, AdminUser.password == password)
            if users.count() > 0:
                session["admin_user_id"] = users[0].id
                return redirect('/admin/index')
            else:
                add_error(u'手机号或密码错误')
    return render_template("admin/login.html", **locals())


@admin.route("/logout", methods=["GET", "POST"])
def admin_logout():
    session["mc_user_id"] = ''
    return redirect('/admin/login')



