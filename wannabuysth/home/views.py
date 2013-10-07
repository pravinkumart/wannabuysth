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
from home import server

index = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@index.route("/help")
def help():
    return render_template("home/help.html", **locals())


@index.route("/accounts")
def accounts():
    return render_template("home/accounts.html", **locals())

@index.route("/regedit")
def regedit():
    return render_template("home/regedit.html", **locals())

@index.route('/forget')
def forget():
    return render_template("home/forget.html", **locals())
@index.route("/forget_do", methods=["POST"])
def forget_do():
    username = request.form.get("username", "")
    code = request.form.get("code", "")
    result = {'succeed':False, 'erro':''}
    if len(username) != 11:
        result['erro'] = '请输入正确的手机号!'
        return jsonify(result)
    if len(code) != 4:
        result['erro'] = '验证码错误!'
        return jsonify(result)
    password = '123456'
    if server.change_password(username, password):
        result = {'succeed':True, 'erro':u'你的新密码是%s' % password}
    else:
        result = {'succeed':False, 'erro':u'帐号错误'}
    return jsonify(result)


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
    try:
        user = Customer(name=name, password=password, mobile=mobile, publish_count=publish_count,
                        success_count=success_count, total_payed=total_payed, fee=fee,
                        current_fee=current_fee,
                        used_fee=used_fee
                        )
        g.db.add(user)
        g.db.commit()
        g.db.flush()
        session["user_id"] = user.id
        result = {'succeed':True, 'erro':user.name}
    except Exception, e:
        result = {'succeed':False, 'erro':u'帐号已存在'}
    return jsonify(result)


@index.route("/login")
def login():
    need_login = request.args.get('need_login', '')
    return render_template("home/login.html", **locals())

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
        session["user_id"] = users[0].id
        result = {'succeed':True, 'erro':users[0].id}
    else:
        result = {'succeed':False, 'erro':'登录失败！请检查帐号和密码'}
    return jsonify(result)

@index.route("/login_out/", methods=['GET', "POST"])
def login_out():
    session["user_id"] = ''
    result = {'succeed':True, 'erro':''}
    return jsonify(result)

@index.route("/index")
def home_index():
    catalogs = g.db.query(Catalog)
    total = catalogs.count()
    catalog_list = [catalogs[i:(i + 8)] for i in range(0, total, 8)]
    user = g.user
    if user:
        notification = server.get_notification(user.id)
    return render_template("home/index.html", **locals())


@index.route("/second_lv/<catalog_id>/")
def second_lv(catalog_id):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(SubCataog).filter(SubCataog.catalog == catalog)
        if sort_type == 1:
            datas = datas.order_by(SubCataog.name)
        total = datas.count()
        catalog_list = [datas[i:(i + 2)] for i in range(0, total, 2)]
    return render_template("home/second_lv.html", **locals())


@index.route("/item_list/<catalog_id>/")
def item_list(catalog_id):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(SubCataog).filter(SubCataog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(Product).filter(Product.catalog == catalog)
        if sort_type:
            datas = datas.order_by(Product.show_fee)
        else:
            datas = datas.order_by(Product.show_fee)
    return render_template("home/item_list.html", **locals())

@index.route("/release/<catalog_id>/")
def release_item(catalog_id):
    if not g.user:
        return redirect(url_for("home.login", need_login="release/%s" % catalog_id))
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(SubCataog).filter(Product.id == catalog_id).first()
    return render_template("home/apply_item.html", **locals())


@index.route("/item_detail/<item_id>/")
def item_detail(item_id):
    sort_type = int(request.args.get("sort_type", '0'))
    item = g.db.query(Product).filter(Product.id == item_id).first()
    return render_template("home/item_detail.html", **locals())




@index.route("/apply_item/<item_id>/")
def apply_item(item_id):
    if not g.user:
        return redirect(url_for("home.login", need_login="apply_item/%s" % item_id))
    sort_type = int(request.args.get("sort_type", '0'))
    item = g.db.query(Product).filter(Product.id == item_id).first()
    return render_template("home/apply_item.html", **locals())


@index.route("/apply_item_do", methods=["POST"])
def apply_item_do():
    import datetime
    import random
    user = g.user
    result = {'succeed':False, 'erro':''}

    item_id = request.form.get("item_id", '')
    catalog_id = request.form.get("catalog_id", '')

    descrip = request.form.get("descrip", '')
    end_time = request.form.get("end_time", '')
    location = request.form.get("location", '')
    wanna_fee = request.form.get("wanna_fee", '')

    if not wanna_fee :
        result['erro'] = '单价输入错误!'
        return jsonify(result)

    try:
        wanna_fee = float(wanna_fee)
    except:
        result['erro'] = '单价输入错误!'
        return jsonify(result)

    if not end_time :
        result['erro'] = '结束时间错误!'
        return jsonify(result)

    try:
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
    except:
        result['erro'] = '结束时间错误!'
        return jsonify(result)

    if not descrip :
        result['erro'] = '描述不能为空!'
        return jsonify(result)
    code = random.randint(1000, 9999)
    req = Requirment(customer_id=user.id, subcataog_id=catalog_id,
                    wanna_fee=wanna_fee * 100, descrip=descrip, end_time=end_time, location=location,
                    state=1, code=code
                    )
    if item_id:
        req.product_id = item_id
    g.db.add(req)
    g.db.commit()
    g.db.flush()
    result = {'succeed':True, 'erro':'%s' % req.id }
    return jsonify(result)


@index.route("/my_keeper")
def my_keeper():
    user = g.user
    if not user:
        return redirect(url_for("home.login", need_login="my_keeper"))
    return render_template("home/my_keeper.html", **locals())



@index.route("/personal")
def personal():
    user = g.user
    if not user:
        return redirect(url_for("home.login", need_login="my_keeper"))
    return render_template("home/personal.html", **locals())


@index.route("/update_user_portrait", methods=["POST"])
def update_user_portrait():
    image = request.form.get("image", "")
    user = g.user
    server.update_user_portrait(user.mobile, image)
    result = {'succeed':False, 'erro':u'帐号错误'}
    return jsonify(result)

@index.route("/choose_item/<requirment_id>")
def choose_item(requirment_id):
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.customer_id == user.id,
                                                Requirment.id == requirment_id).first()
    return render_template("home/choose_item.html", **locals())


@index.route("/choose_list")
def choose_list():
    user = g.user
    datas = g.db.query(Requirment).filter(Requirment.customer_id == user.id, Requirment.state == 2)
    return render_template("home/choose_list.html", **locals())


@index.route("/decide_item/<requirment_id>")
def decide_item(requirment_id):
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.customer_id == user.id,
                                                Requirment.id == requirment_id).first()
    if requirment:
        replys = g.db.query(Reply).filter(Reply.requirment_id == requirment.id)
    return render_template("home/decide_item.html", **locals())


@index.route("/decide_list")
def decide_list():
    '''
    @note: 显示状态为  0 1
    '''
    user = g.user
    datas = g.db.query(Requirment).filter(Requirment.customer_id == user.id, Requirment.state.in_([0, 1]))
    return render_template("home/decide_list.html", **locals())

@index.route("/admin_list")
def admin_list():
    '''
    '''
    user = g.user
    datas = g.db.query(Requirment).filter(Requirment.state != -1)
    return render_template("home/admin_list.html", **locals())


@index.route("/admin_item/<requirment_id>")
def admin_item(requirment_id):
    import random
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.customer_id == user.id,
                                                Requirment.id == requirment_id).first()
    if requirment:
        rc = Reply(requirment_id=requirment.id, merchant_id=1, fee=random.randint(100, 200), descrip=u'自动生成')
        g.db.add(rc)
        g.db.commit()
    return redirect(url_for("home.admin_list"))

@index.route("/select_reply/<reply_id>", methods=["POST"])
def select_reply_do(reply_id):
    user = g.user
    reply = g.db.query(Reply).filter(Reply.id == reply_id).first()
    if reply:
        merchant = reply.merchant
        requirment = reply.requirment
        requirment.merchant_id = merchant.id
        requirment.state = 2
        g.db.add(requirment)
        g.db.commit()
    result = {'succeed':True, 'erro':user.name}
    return jsonify(result)

@index.route("/update_choose_item/<requirment_id>", methods=["POST"])
def update_choose_item(requirment_id):
    code = request.form.get("code", '')
    state = request.form.get("state", '')
    requirment = g.db.query(Requirment).filter(Requirment.id == requirment_id).first()
    if requirment and requirment.code == code and state:
        state = int(state)
        requirment.state = state
        if state == 4 and requirment.product:
            product = requirment.product
            product.success_count = product.success_count + 1
            g.db.add(product)
        g.db.add(requirment)
        g.db.commit()
        result = {'succeed':True, 'erro':u''}
    else:
        result = {'succeed':False, 'erro':u'交易码错误'}
    return jsonify(result)

@index.route("/choose_f/<reply_id>", methods=["POST"])
def choose_f(reply_id):
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.id == reply_id).first()
    requirment.state = 3
    g.db.add(requirment)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)



@index.route("/choose_s/<reply_id>", methods=["POST"])
def choose_s(reply_id):
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.id == reply_id).first()
    requirment.state = 4
    g.db.add(requirment)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)


@index.route("/choose_d/<reply_id>", methods=["POST"])
def choose_d(reply_id):
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.id == reply_id).first()
    requirment.state == -1
    g.db.add(requirment)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)

@index.route("/history_list")
def history_list():
    user = g.user
    sort_type = int(request.args.get("sort_type", '0'))
    datas = g.db.query(Requirment).filter(Requirment.customer_id == user.id, Requirment.state.in_([3, 4]))
    if sort_type == 0:
        datas = datas.order_by(Requirment.id)
    else:
        datas = datas.order_by(Requirment.wanna_fee)
    return render_template("home/history_list.html", **locals())


@index.route("/setings")
def setings():
    return render_template("home/setings.html", **locals())



@index.route("/update_mobile")
def update_mobile():
    user = g.user
    return render_template("home/update_mobile.html", **locals())


@index.route("/update_user_mobile", methods=["POST"])
def update_user_mobile():
    mobile = request.form.get("mobile", "").strip()
    password = request.form.get("password", "")
    succeed, erro = False, u'密码错误'
    user = g.user
    if user.password == password:
        if mobile == user.mobile:
            return jsonify({'succeed':True, 'erro':'保存成功'})
        succeed, erro = server.update_user_mobile(user.id, mobile)
    result = {'succeed':succeed, 'erro':erro}
    return jsonify(result)


@index.route("/update_user_password", methods=["POST"])
def update_user_password():
    new_password = request.form.get("new_password", "").strip()
    password = request.form.get("password", "")
    succeed, erro = False, u'旧密码错误'
    user = g.user
    if user.password == password:
        succeed, erro = server.update_user_password(user.id, new_password)
    result = {'succeed':succeed, 'erro':erro}
    return jsonify(result)

@index.route("/update_name")
def update_name():
    user = g.user
    return render_template("home/update_name.html", **locals())

@index.route("/update_user_name", methods=["POST"])
def update_user_name():
    username = request.form.get("username", "").strip()
    user = g.user
    if username == user.name:
        return jsonify({'succeed':True, 'erro':'保存成功'})
    succeed, erro = server.update_user_name(user.mobile, username)
    result = {'succeed':succeed, 'erro':erro}
    return jsonify(result)


@index.route("/update_password")
def update_password():
    return render_template("home/update_password.html", **locals())


@index.route("/sell_list")
def sell_list():
    return render_template("home/sell_list.html", **locals())

@index.route("/bijia")
def bijia():
    return render_template("home/bijia.html", **locals())



@index.route("/location")
def location():
    return render_template("home/location.html", **locals())







