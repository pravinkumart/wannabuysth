# -*- coding: UTF-8 -*-
__author__ = 'alex'

import logging
from flask import Blueprint, render_template, abort, g, request
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import Customer
from models import Catalog
from models import SubCataog
from models import Product
from models import Requirment, Reply
from models import Merchant, CustomerCataog
from utils import add_error, add_success

mc = Blueprint('mc', __name__, template_folder='templates', url_prefix='/mc')


@mc.route("/login", methods=["GET", "POST"])
def mc_login():
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if not username or not password:
            add_error(u'手机号或密码不能为空')
        else:
            users = g.db.query(Merchant).filter(Merchant.mobile == username, Merchant.password == password)
            if users.count() > 0:
                session["mc_user_id"] = users[0].id
                return redirect('/mc/index')
            else:
                add_error(u'手机号或密码错误')
    return render_template("mc/login.html", **locals())


@mc.route("/logout", methods=["GET", "POST"])
def mc_logout():
    session["mc_user_id"] = ''
    return redirect('/mc/index')



@mc.route("/", methods=["GET", "POST"])
@mc.route("/index", methods=["GET", "POST"])
def mc_index():
    if not g.mc_user:
        return redirect('/mc/login')
    else:
        mc_user = g.mc_user
        if not g.db.query(CustomerCataog).filter(CustomerCataog.customer_id == mc_user.id).first():
            return redirect('/mc/product/catalog')
        else:
            return redirect('/mc/requirment/0')

@mc.route("/requirment/<requirment_id>", methods=["GET", "POST"])
def requirment_show(requirment_id):
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    requirment_id = int(requirment_id)
    replys = g.db.query(Reply).filter(Reply.merchant_id == mc_user.id)
    requirment_ids = [reply.requirment_id for reply in replys]
    if requirment_id == 0:
        my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.customer_id == mc_user.id)
        mu_subcataog_ids = [rec.catalog_id  for rec in my_subcatalogs]
        datas = g.db.query(Requirment).filter(Requirment.state.in_([0, 1]), Requirment.subcataog_id.in_(mu_subcataog_ids))
    if requirment_id == 2:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state == 2)
    if requirment_id == 3:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state.in_([3, 4]))
    return render_template("mc/requirment_%s.html" % requirment_id, **locals())


@mc.route("/requirment/reply/<requirment_id>", methods=["GET", "POST"])
def requirment_reply(requirment_id):
    from models import Notification
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    requirment_id = int(requirment_id)
    my_fee = int(float(request.args.get("my_fee", "0").strip()) * 100)
    rec = Reply(requirment_id=requirment_id, merchant_id=mc_user.id, fee=my_fee, descrip='')
    g.db.add(rec)
    g.db.commit()
    # 通知用户
    url = 'item_detail'
    content = '商家%s回应了你的发布' % rec.merchant.name
    rec = Notification(customer_id=rec.requirment.customer_id, content=content, type=1, url=url)
    g.db.add(rec)
    g.db.commit()


    return redirect('/mc/requirment/0')

@mc.route("/requirment/reset_code/<requirment_id>", methods=["GET", "POST"])
def requirment_reset_code(requirment_id):
    import random
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    requirment_id = int(requirment_id)
    rec = g.db.query(Requirment).filter(Requirment.id == requirment_id, Requirment.merchant_id == mc_user.id).first()
    if rec:
        rec.code = random.randint(1000, 9999)
        g.db.add(rec)
        g.db.commit()
    return redirect('/mc/requirment/2')


@mc.route("/product/list", methods=["GET", "POST"])
def product_list():
    if not g.mc_user:
        return redirect('/mc/login')

    mc_user = g.mc_user
    return render_template("mc/product_list.html" , **locals())

@mc.route("/regedit", methods=["GET", "POST"])
def mc_regedit():
    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        password = request.form.get("password", "")
        re_password = request.form.get("re_password", "")

        if not mobile or not password:
            add_error(u'手机号或密码不能为空')
        elif not mobile or len(mobile) != 11:
            add_error(u'请输入11位手机号')
        elif password != re_password:
            add_error(u'2次输入的密码不一致')
        elif g.db.query(Merchant).filter(Merchant.mobile == mobile).first():
            add_error(u'手机号已使用')
        elif g.db.query(Merchant).filter(Merchant.name == name).first():
            add_error(u'商家名称已使用')
        else:
            rec = Merchant(name=name, mobile=mobile, password=password, pre_payed=0,
                           success_count=0, faild_count=0, catalog_count=1, subcatalog_count=3
                           )
            g.db.add(rec)
            g.db.commit()
            session["mc_user_id"] = rec.id
            return redirect('/mc/index')
    return render_template("mc/regedit.html", **locals())


@mc.route("/product/catalog", methods=["GET", "POST"])
def mc_catalog():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    catalog_type = request.args.get("type", "").strip()
    if catalog_type:
        catalog = g.db.query(Catalog).filter(Catalog.id == catalog_type, Catalog.status == True).first()
        if catalog:
            subcatalogs = g.db.query(SubCataog).filter(SubCataog.catalog_id == catalog.id, SubCataog.status == True)

    else:
        catalogs = g.db.query(Catalog).filter(Catalog.status == True)

    my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.customer_id == mc_user.id)
    my_subcatalogs = [rec.catalog for rec in my_subcatalogs]
    if request.method == 'POST':
        has_data = g.db.query(CustomerCataog).filter(CustomerCataog.customer_id == mc_user.id)
        has_data.delete()
        subcatalogs = request.form.getlist('subcatalog')
        for i, catalog_id in enumerate(subcatalogs):
            if i > 2:
                continue
            add_sub = CustomerCataog(catalog_id=catalog_id, customer_id=mc_user.id)
            g.db.add(add_sub)
        g.db.commit()
        return redirect('/mc/product/catalog')
    return render_template("mc/catalog.html", **locals())


@mc.route("/product/product", methods=["GET", "POST"])
def mc_product():
    if not g.mc_user:
        return redirect('/mc/login')
    catalogs = g.db.query(Catalog).filter(Catalog.status == True)
    mc_user = g.mc_user
    return render_template("mc/product.html", **locals())






