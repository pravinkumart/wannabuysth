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
from models import Merchant
from utils import add_error, add_success

mc = Blueprint('mc', __name__, template_folder='templates', url_prefix='/mc')


@mc.route("/login", methods=["GET", "POST"])
def mc_login():
    if request.method == 'POST':
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if not username or not password:
            add_error(u'帐号或密码不能为空')
        else:
            users = g.db.query(Merchant).filter(Merchant.mobile == username, Merchant.password == password)
            if users.count() > 0:
                session["mc_user_id"] = users[0].id
                return redirect('/mc/index')
            else:
                add_error(u'帐号或密码错误')
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
        datas = g.db.query(Requirment).filter(Requirment.state.in_([0, 1]))
    if requirment_id == 2:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state == 2)
    if requirment_id == 3:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state.in_([3, 4]))
    return render_template("mc/requirment_%s.html" % requirment_id, **locals())


@mc.route("/requirment/reply/<requirment_id>", methods=["GET", "POST"])
def requirment_reply(requirment_id):
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    requirment_id = int(requirment_id)
    rec = Reply(requirment_id=requirment_id, merchant_id=mc_user.id, fee=0, descrip='')
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

