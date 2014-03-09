# -*- coding: UTF-8 -*-
__author__ = 'alex'

import logging
from flask import Blueprint, render_template, abort, g, request
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import Customer
from models import Catalog
from models import SubCatlog
from models import Product, SuccessRequirment
from models import Requirment, Reply
from models import ProductAds, Comments, Notification
from models import ShowCase, ShowCaseReplay, UserExternalBind
from home import server
from datetime import datetime

index = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')


@index.route("/help")
def help_me():
    return render_template("home/help.html", **locals())

@index.route("/loading")
def loading():
    return render_template("home/loading.html", **locals())

@index.route("/about")
def about():
    return render_template("home/about.html", **locals())


@index.route("/catalog_search")
def catalog_search():
    return render_template("home/catalog_search.html", **locals())

@index.route("/notification")
def notification():
    sort_type = int(request.args.get("sort_type", '0'))
    user = g.user
    if not user:
        return redirect(url_for("home.login", need_login="my_keeper"))

    datas = g.db.query(Notification).filter(Notification.customer_id == user.id)
    if sort_type == 0:
        datas = datas.filter(Notification.type == 1).order_by(Notification.id)
    else:
        datas = datas.filter(Notification.type == 0).order_by(Notification.id)
    return render_template("home/notification.html", **locals())

@index.route("/notification/read", methods=["POST"])
def notification_read():
    sort_type = int(request.args.get("sort_type", '0'))
    user = g.user
    if user:
        g.db.query(Notification).filter(Notification.customer_id == user.id).update({Notification.is_visit:True})
        g.db.commit()
    return jsonify({})


@index.route("/accounts")
def accounts():
    return render_template("home/accounts.html", **locals())

@index.route("/regedit")
def regedit():
    return render_template("home/regedit.html", **locals())


@index.route("/proxy")
def proxy():
    next = request.args.get("next", "")
    return render_template("home/proxy.html", **locals())

@index.route("/oauth")
def oauth():
    from home.server import QQOAuth2Mixin
    qq = QQOAuth2Mixin()
    request_url = qq.get_authorize_redirect()
    return render_template("home/oauth.html", **locals())


@index.route("/oauth/w")
def oauth_w():
    from home.server import QQOAuth2Mixin
    qq = QQOAuth2Mixin()
    request_url = qq.get_authorize_redirect(display="web")
    return redirect(request_url)

@index.route("/oauth/qq")
def oauth_qq():
    from models import Merchant
    display = request.args.get("display", "")
    if display == 'web':
        mc_user = g.db.query(Merchant).filter(Merchant.mobile == '15982150122')
        if mc_user:
            code = request.args.get("code", "")
            from home.server import QQOAuth2Mixin
            qq = QQOAuth2Mixin()
            if code:
                content = qq.get_authenticated_user(code)
                access_token = content['access_token']
                refresh_token = content['refresh_token']
                openid = content['openid']
                user_info = qq.get_user_info(access_token, openid)
                name = user_info['nickname']
                mc_user[0].name = name
                try:
                    g.db.add(mc_user[0])
                    g.db.commit()
                except:
                    pass
            session['mc_user_id'] = mc_user[0].id
            return redirect('/mc')
        else:
            raise
            return redirect('/')
    import random
    from home.server import QQOAuth2Mixin
    qq = QQOAuth2Mixin()
    code = request.args.get("code", "")
    if code:
        content = qq.get_authenticated_user(code)
        if content.has_key('openid'):
            openid = content['openid']
            access_token = content['access_token']
            refresh_token = content['refresh_token']
            userbind = g.db.query(UserExternalBind).filter(UserExternalBind.external_user_id == openid,
                                                         UserExternalBind.source == 'qq').first()
            if userbind:
                userbind.access_token = access_token
                userbind.refresh_token = refresh_token
                g.db.add(userbind)
                g.db.commit()
                session["user_id"] = userbind.customer_id
                return redirect('/home/proxy?next=index')
            else:
                user_info = qq.get_user_info(access_token, openid)
                name = user_info['nickname']
                if g.db.query(Customer).filter(Customer.name == name).first():
                    name = '%s' % int(time.time() * 1000)
                mobile = 'q%s%s' % (random.randint(10000, 99999), random.randint(10000, 99999))
                user = Customer(name=name, password=mobile, mobile=mobile, publish_count=0,
                   success_count=0, total_payed=0, fee=0,
                   current_fee=0,
                   used_fee=0
                   )
                g.db.add(user)
                g.db.commit()

                userbind = UserExternalBind(access_token=access_token, refresh_token=refresh_token,
                                            external_user_id=openid, source='qq', customer_id=user.id
                                            )
                g.db.add(userbind)
                g.db.commit()
                session["user_id"] = user.id
                return redirect('/home/proxy?next=index')
    return redirect('/home/proxy?next=login')


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
    from home.server import QQOAuth2Mixin
    qq = QQOAuth2Mixin()
    request_url = qq.get_authorize_redirect()
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
        user = users[0]
        if user.status:
            session["user_id"] = user.id
            result = {'succeed':True, 'erro':users[0].id}
        else:
            result = {'succeed':False, 'erro':u'帐号被禁止'}
    else:
        result = {'succeed':False, 'erro':u'登录失败！请检查帐号和密码'}
    return jsonify(result)

@index.route("/login_out/", methods=['GET', "POST"])
def login_out():
    session["user_id"] = ''
    result = {'succeed':True, 'erro':''}
    return jsonify(result)

@index.route("/index")
def home_index():
    now = datetime.now()

    user = g.user
    if user:
        if user.mobile[0] == 'q':
            return redirect('/home/bind_mobile')
        notification = server.get_notification(user.id)

    # 今日推荐
    ad = g.db.query(ProductAds).filter(ProductAds.type == 0, ProductAds.start_time <= now,
                                             ProductAds.end_time >= now).order_by(ProductAds.sort_num).first()

    catalogs = g.db.query(Catalog).order_by(Catalog.idx.desc()) 
    total = catalogs.count()
    catalog_list = [catalogs[i:(i + 2)] for i in range(0, total, 2)]
    logging.error("index-catalogs:\n%s" % catalog_list)
    return render_template("home/index.html", **locals())


@index.route("/second_lv/<catalog_id>/")
def second_lv(catalog_id):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(SubCatlog).filter(SubCatlog.catalog == catalog)
        if sort_type == 1:
            datas = datas.order_by(SubCatlog.pingying)
        else:
            datas = datas.order_by(SubCatlog.count)
        total = datas.count()
        catalog_list = [datas[i:(i + 2)] for i in range(0, total, 2)]
    return render_template("home/second_lv.html", **locals())

@index.route("/catalog/<catalog_id>/")
def catalog(catalog_id):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(SubCatlog).filter(SubCatlog.catalog == catalog)
        if sort_type == 1:
            datas = datas.order_by(SubCatlog.pingying)
        else:
            datas = datas.order_by(SubCatlog.count)
        total = datas.count()
        catalog_list = [datas[i:(i + 2)] for i in range(0, total, 2)]
    return render_template("home/sub_catalog_list.html", **locals())

@index.route("/catalog/<catalog_id>/<my_fee>")
def catalog_my_fee(catalog_id, my_fee):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(Catalog).filter(Catalog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(SubCatlog).filter(SubCatlog.catalog == catalog)
        if sort_type == 1:
            datas = datas.order_by(SubCatlog.pingying)
        else:
            datas = datas.order_by(SubCatlog.count)
        total = datas.count()
        catalog_list = [datas[i:(i + 2)] for i in range(0, total, 2)]
        for catalogs in catalog_list:
            for catalog in catalogs:
                catalog.ucount = g.db.query(Product).filter(Product.show_fee < float(my_fee) * 100, Product.catalog_id == catalog.id, Product.status == True).count()
    return render_template("home/sub_catalog_list.html", **locals())

@index.route("/item_list/<catalog_id>/")
@index.route("/item_list/<catalog_id>/<my_fee>")
def item_list(catalog_id, my_fee=None):
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(SubCatlog).filter(SubCatlog.id == catalog_id).first()
    if catalog:
        datas = g.db.query(Product).filter(Product.catalog == catalog, Product.status == True)
        if sort_type == 0:
            datas = datas.order_by(Product.show_fee.desc())
        else:
            datas = datas.order_by(Product.show_fee.asc())
        if my_fee:
            datas = datas.filter(Product.show_fee < float(my_fee) * 100)
    return render_template("home/item_list.html", **locals())

@index.route("/release/<catalog_id>/")
def release_item(catalog_id):
    if not g.user:
        return redirect(url_for("home.login", need_login="release/%s" % catalog_id))
    sort_type = int(request.args.get("sort_type", '0'))
    catalog = g.db.query(SubCatlog).filter(SubCatlog.id == catalog_id).first()
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
    auto = True if  request.args.get("auto", '') == 'true' else False
    item = g.db.query(Product).filter(Product.id == item_id).first()
    return render_template("home/apply_item.html", **locals())


@index.route("/apply_item_do", methods=["POST"])
def apply_item_do():
    import random
    user = g.user
    result = {'succeed':False, 'erro':''}

    item_id = request.form.get("item_id", '')
    catalog_id = request.form.get("catalog_id", '')

    descrip = request.form.get("descrip", '')
    end_time = request.form.get("end_time", '')
    location = request.form.get("location", '')
    wanna_fee = request.form.get("wanna_fee", '')

    auto = request.form.get("auto", '')

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
        end_time = datetime.strptime(end_time, "%Y-%m-%d")
    except:
        result['erro'] = '结束时间错误!'
        return jsonify(result)

    if not descrip :
        result['erro'] = '描述不能为空!'
        return jsonify(result)
    code = random.randint(1000, 9999)
    req = Requirment(customer_id=user.id, subcatlog_id=catalog_id,
                    wanna_fee=wanna_fee * 100, descrip=descrip, end_time=end_time, location=location,
                    state=1, code=code
                    )
    if item_id:
        req.product_id = item_id
    g.db.add(req)
    g.db.commit()
    if auto == 'true':
            req.merchant_id = req.product.merchant_id
            req.state = 2
            g.db.add(req)
            g.db.commit()

            r = Reply(requirment_id=req.id, merchant_id=req.merchant_id, fee=req.product.show_fee)
            g.db.add(r)
            g.db.commit()

            req.reply_id = r.id
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

    reply = g.db.query(Reply).filter(Reply.id == requirment.reply_id).first()
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
        requirment.reply_id = reply.id
        requirment.state = 2
        g.db.add(requirment)
        g.db.commit()
    result = {'succeed':True, 'erro':user.name}
    return jsonify(result)

@index.route("/update_choose_item/<requirment_id>", methods=["POST"])
def update_choose_item(requirment_id):
    code = request.form.get("code", '')
    state = 3  # request.form.get("state", '')
    state = int(state)
    like = int(request.form.get("state", '1'))
    user = g.user
    requirment = g.db.query(Requirment).filter(Requirment.id == requirment_id, Requirment.customer_id == user.id).first()
    if requirment and requirment.code == code and state:
        state = int(state)
        requirment.state = state
        if state == 3 and requirment.product:
            product = requirment.product
            product.success_count = product.success_count + 1
            g.db.add(product)

            reply = g.db.query(Reply).filter(Reply.id == requirment.reply_id).first()

            re = SuccessRequirment(customer_id=requirment.customer_id, merchant_id=requirment.merchant_id, wanna_fee=requirment.wanna_fee,
                              descrip=requirment.descrip, end_time=requirment.end_time, location=requirment.location,
                              succes_fee=reply.fee, reply_id=requirment.reply_id, product_id=requirment.product_id,
                              subcatlog_id=requirment.subcatlog_id , like=like
                              )
            g.db.add(re)
            g.db.commit()
            user.current_fee += reply.fee * 0.1
            user.user_level += 2
            g.db.add(user)
            g.db.commit()
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
    oper = request.form.get("oper", "").strip()
    mobile = request.form.get("mobile", "").strip()
    password = request.form.get("password", "")
    succeed, erro = False, u'密码错误'
    user = g.user
    if oper == 'bind':
        succeed, erro = server.update_bind_mobile(user, mobile, password)
    elif user.password == password:
        if mobile == user.mobile:
            return jsonify({'succeed':True, 'erro':'保存成功'})
        succeed, erro = server.update_user_mobile(user.id, mobile)
    result = {'succeed':succeed, 'erro':erro}
    return jsonify(result)


@index.route("/bind_mobile")
def bind_mobile():
    user = g.user
    return render_template("home/bind_mobile.html", **locals())


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
    user = g.user
    now = datetime.now()
    ad_index = g.db.query(ProductAds).filter(ProductAds.type == 1, ProductAds.start_time <= now,
                                             ProductAds.end_time >= now).order_by(ProductAds.sort_num).first()
    ads = g.db.query(ProductAds).filter(ProductAds.type == 2, ProductAds.start_time <= now,
                                             ProductAds.end_time >= now).order_by(ProductAds.sort_num)
    ads = [ads[i:(i + 2)] for i in range(0, ads.count(), 2)]
    return render_template("home/sell_list.html", **locals())

@index.route("/bijia")
def bijia():
    user = g.user
    sort_type = int(request.args.get("sort_type", '0'))
    if sort_type:
        showcases = g.db.query(ShowCase).order_by(ShowCase.wanna_fee.desc())
    else:
        showcases = g.db.query(ShowCase).order_by(ShowCase.wanna_fee.asc())
    return render_template("home/bijia_list.html", **locals())



@index.route("/location")
def location():
    return render_template("home/location.html", **locals())

@index.route("/share_requirment")
def share_requirment():
    user = g.user
    if not user:
        return redirect(url_for("home.login", need_login="share_requirment"))

    showcases = g.db.query(ShowCase).filter(ShowCase.customer_id == user.id).\
    order_by(ShowCase.id)

    showcases_ids = [showcase.requirment_id  for showcase in showcases]

    requirments = g.db.query(SuccessRequirment).filter(SuccessRequirment.customer_id == user.id).\
    order_by(SuccessRequirment.id)

    return render_template("home/share_requirment.html", **locals())




@index.route("/share_requirment/<requirment_id>", methods=["POST"])
def share_requirment_id(requirment_id):
    user = g.user
    requirment = g.db.query(SuccessRequirment).filter(SuccessRequirment.id == requirment_id).first()
    if not requirment:
        result = {'succeed':False, 'erro':'找不到id'}
        return jsonify(result)

    if  g.db.query(ShowCase).filter(ShowCase.requirment_id == requirment_id).first():
        result = {'succeed':False, 'erro':'已经发布过了'}
        return jsonify(result)

    rec = ShowCase(requirment_id=requirment_id, customer_id=user.id, wanna_fee=requirment.wanna_fee)
    g.db.add(rec)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)



@index.route("/bijia_detail/<showcase_id>")
def bijia_detail(showcase_id):
    showcase = g.db.query(ShowCase).filter(ShowCase.id == showcase_id).first()
    sort_type = int(request.args.get("sort_type", '0'))
    if sort_type:
        showcases = g.db.query(ShowCaseReplay).filter(ShowCaseReplay.showcase_id == showcase_id).order_by(ShowCaseReplay.wanna_fee.desc())
    else:
        showcases = g.db.query(ShowCaseReplay).filter(ShowCaseReplay.showcase_id == showcase_id).order_by(ShowCaseReplay.wanna_fee.asc())


    comments = g.db.query(Comments).filter(Comments.showcase_id == showcase_id).order_by(Comments.id.asc())

    return render_template("home/bijia_detail.html", **locals())



@index.route("/comment/<showcase_id>", methods=["POST"])
def comment_showcase(showcase_id):
    content = request.form.get("content", "").strip()
    user = g.user
    rec = Comments(showcase_id=showcase_id, customer_id=user.id, content=content)
    g.db.add(rec)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)

@index.route("/show_casereplay/<showcase_id>")
def show_casereplay(showcase_id):
    user = g.user
    if not user:
        return redirect(url_for("home.login", need_login="show_casereplay/%s" % showcase_id))
    showcase = g.db.query(ShowCase).filter(ShowCase.id == showcase_id).first()
    subcatlog_id = showcase.requirment.subcatlog_id
    showcases = g.db.query(SuccessRequirment).filter(SuccessRequirment.customer_id == user.id)
    
    have_cases = g.db.query(ShowCaseReplay).filter(ShowCaseReplay.customer_id == user.id)
    have_cases = [have_case.requirment_id for have_case in have_cases]
    
    showcases = [showcase  for showcase in showcases if showcase.subcatlog_id == subcatlog_id and showcase.id not in have_cases]
    
    return render_template("home/bijia_casereplay.html", **locals())


@index.route("/re_showcase/<showcase_id>/<showcase_re_id>", methods=["POST"])
def re_showcase(showcase_id, showcase_re_id):
    showcase_re = g.db.query(SuccessRequirment).filter(SuccessRequirment.id == showcase_re_id).first()


    rec = ShowCaseReplay(showcase_id=showcase_id , requirment_id=showcase_re_id,
                   customer_id=showcase_re.customer_id, wanna_fee=showcase_re.wanna_fee)
    g.db.add(rec)
    g.db.commit()
    result = {'succeed':True, 'erro':''}
    return jsonify(result)

@index.route("/catalog_list", methods=["GET"])
def catalog_list():
    catalogs = g.db.query(Catalog).filter(Catalog.status == True).order_by(Catalog.idx)
    catalog_list = [catalogs[i:(i + 2)] for i in range(0, catalogs.count(), 2)]
    return render_template("home/catalog_list.html", **locals())

@index.route("/catalog_list/<my_fee>", methods=["GET"])
def catalog_list_my_fee(my_fee):
    catalogs = g.db.query(Catalog).filter(Catalog.status == True).order_by(Catalog.idx)

    catalog_list = [catalogs[i:(i + 2)] for i in range(0, catalogs.count(), 2)]
    for catalogs in catalog_list:
        for catalog in catalogs:
            subs = g.db.query(SubCatlog).filter(SubCatlog.catalog_id == catalog.id)
            sub_ids = [sub.id for sub in subs]
            catalog.ucount = g.db.query(Product).filter(Product.show_fee < float(my_fee) * 100, Product.catalog_id.in_(sub_ids), Product.status == True).count()

    return render_template("home/catalog_list.html", **locals())


@index.route("/delete_bijia/<data_id>", methods=["GET", 'POST'])
def delete_bijia(data_id):
    result = {'succeed':True, 'erro':''}
    user = g.user
    if not user:
        return jsonify(result)
    
    showcase = g.db.query(ShowCase).filter(ShowCase.id == data_id, ShowCase.customer_id == user.id).first()
    if showcase:
        have_cases = g.db.query(ShowCaseReplay).filter(ShowCaseReplay.customer_id == user.id, ShowCaseReplay.showcase == showcase)
        for have_case in have_cases:
            g.db.delete(have_case)
            
        comments = g.db.query(Comments).filter(Comments.customer_id == user.id, Comments.showcase == showcase)
        for comment in comments:
            g.db.delete(comment)
            
        g.db.delete(showcase)
        g.db.commit()
    
    return jsonify(result)







