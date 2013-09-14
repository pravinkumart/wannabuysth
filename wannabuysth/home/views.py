# -*- coding: UTF-8 -*-
__author__ = 'alex'

import logging
from tempfile import NamedTemporaryFile
from flask import Blueprint, render_template, abort, g, request
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
from models import Customer
import time


index = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@index.route("/help")
def help():
    return render_template("help.html", **locals())


@index.route("/accounts")
def accounts():
    return render_template("accounts.html", **locals())

@index.route("/regedit")
def regedit():
    return render_template("regedit.html", **locals())



@index.route("/regedit_do", methods=["POST"])
def regedit_do():
    username = request.form.get("username", "")
    re_password = request.form.get("re_password", "")
    password = request.form.get("password", "")
    result = {'succeed':False, 'erro':''}
    if len(username) != 11:
        result['erro'] = '请输入正确的手机号!'
        return jsonify(result)
    if not password or len(password) < 6:
        result['erro'] = '密码不能小于6位数!'
        return jsonify(result)
    if password != re_password:
        result['erro'] = '两次密码不一致!'
        return jsonify(result)

    name = '%s' % int(time.time() * 1000)
    password = password
    mobile = username
    publish_count = 0
    success_count = 0
    total_payed = 0
    fee = 0
    current_fee = 0
    used_fee = 0

    user = Customer(name=name, password=password, mobile=mobile, publish_count=publish_count,
                    success_count=success_count, total_payed=total_payed, fee=fee, current_fee=current_fee,
                    used_fee=used_fee
                    )
    g.db.add(user)
    g.db.commit()
    g.db.flush()
    session["user_id"] = name
    result = {'succeed':True, 'erro':user.name}
    return jsonify(result)


@index.route("/login")
def login():
    return render_template("login.html", **locals())

@index.route("/login_do", methods=["POST"])
def login_do():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    result = {'succeed':False, 'erro':''}
    if len(username) != 11:
        result['erro'] = '请输入正确的手机号!'
        return jsonify(result)

    users = g.db.query(Customer).filter(Customer.mobile == username, Customer.password == password)
    if users.count() > 0:
        session["user_id"] = users[0].name
        result = {'succeed':True, 'erro':users[0].name}
    else:
        result = {'succeed':False, 'erro':'登录失败！请检查帐号和密码'}
    return jsonify(result)

@index.route("/forget")
def forget():
    return render_template("forget.html", **locals())
