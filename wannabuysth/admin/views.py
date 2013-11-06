# -*- coding: UTF-8 -*-
import logging
from flask import Blueprint, render_template, abort, g, request
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import AdminUser
from datetime import datetime
from utils import add_error, add_success
from models import Catalog, SubCatlog

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
            add_error(u'帐号或密码不能为空')
        else:
            users = g.db.query(AdminUser).filter(AdminUser.name == username, AdminUser.password == password)
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

@admin.route("/catalog", methods=["GET", "POST"])
def catalog():
    if not g.admin_user:
        return redirect('/admin/login')
    cu_catalog = int(request.args.get("catalog", "0"))
    admin_user = g.admin_user


    if request.method == 'POST':
        name = request.form.get("name", "")
        descp = request.form.get("descp", "")
        icon_smaill = request.form.get("icon_smaill", "")
        icon_large = request.form.get("icon_large", "")
        idx = request.form.get("idx", "0")

        if not name or not icon_smaill:
            add_error(u'名字或者图片不能为空')
        else:
            if g.db.query(Catalog).filter(Catalog.name == name).first():
                add_error(u'频道名字已存在')
            else:
                c = Catalog(name=name, descp=descp, icon_smaill=icon_smaill, icon_large=icon_large, idx=idx)
                g.db.add(c)
                g.db.commit()
                add_success(u'频道添加成功')
                return redirect('/admin/catalog')
    catalogs = g.db.query(Catalog).all()
    if not cu_catalog == 0:
        subcatlogs = g.db.query(SubCatlog).filter(SubCatlog.catalog_id == cu_catalog)
    return render_template("admin/catalog.html", **locals())


@admin.route("/catalog/<catalog_id>/del", methods=["GET", "POST"])
def catalog_del(catalog_id):
    if not g.admin_user:
        return redirect('/admin/login')
    data = g.db.query(Catalog).filter(Catalog.id == catalog_id).first()
    g.db.delete(data)
    g.db.commit()
    add_success(u'成功删除频道')
    return redirect('/admin/catalog')


@admin.route("/subcatlog/<subcatlog_id>/del", methods=["GET", "POST"])
def subcatlog_del(subcatlog_id):
    if not g.admin_user:
        return redirect('/admin/login')
    data = g.db.query(SubCatlog).filter(SubCatlog.id == subcatlog_id).first()
    catalog_id = data.catalog_id
    g.db.delete(data)
    g.db.commit()
    add_success(u'成功删除频道')
    return redirect('/admin/catalog?catalog=%s' % catalog_id)



@admin.route("/catalog/<cu_catalog>", methods=["GET", "POST"])
def sub_catalog(cu_catalog):
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    cu_catalog = int(cu_catalog)

    if request.method == 'POST':
        name = request.form.get("name", "")
        descp = request.form.get("descp", "")
        icon_smaill = request.form.get("icon_smaill", "")
        icon_large = request.form.get("icon_large", "")
        idx = request.form.get("idx", "0")
        pingying = request.form.get("pingying", "")

        if not name or not icon_smaill:
            add_error(u'名字或者图片不能为空')
        else:
            if g.db.query(SubCatlog).filter(SubCatlog.name == name).first():
                add_error(u'频道名字已存在')
            else:
                c = SubCatlog(catalog_id=cu_catalog, name=name, pingying=pingying, descp=descp, icon_smaill=icon_smaill, icon_large=icon_large, idx=idx)
                g.db.add(c)
                g.db.commit()
                add_success(u'子频道添加成功')
                return redirect('/admin/catalog?catalog=%s' % cu_catalog)
    catalogs = g.db.query(Catalog).all()
    if not cu_catalog == 0:
        subcatlogs = g.db.query(SubCatlog).filter(SubCatlog.catalog_id == cu_catalog)
    return render_template("admin/sub_catalog.html", **locals())
