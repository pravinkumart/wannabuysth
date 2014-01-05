# -*- coding: UTF-8 -*-
__author__ = 'alex'

import logging
from flask import Blueprint, render_template, abort, g, request, Response
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import Customer
from models import Catalog
from models import SubCatlog
from models import Product, MerchantPayed
from models import Requirment, Reply
from models import Merchant, CustomerCataog, SuccessRequirment
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
                if users[0].status:
                    session["mc_user_id"] = users[0].id
                else:
                    add_error(u'帐号被禁止')
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
        if not g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id).first():
            return redirect('/mc/product/add_catalog')
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
        my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id)
        mu_subcatlog_ids = [rec.catalog_id  for rec in my_subcatalogs]
        datas = g.db.query(Requirment).filter(Requirment.state.in_([0, 1]), Requirment.subcatlog_id.in_(mu_subcatlog_ids))
        r_min = request.args.get("min", "0").strip()
        r_max = request.args.get("max", "").strip()
        index = request.args.get("index", "0").strip()
        try:
            r_min = float(r_min)
            datas = datas.filter(Requirment.wanna_fee > r_min * 100)
        except:
            pass
        try:
            r_max = float(r_max)
            datas = datas.filter(Requirment.wanna_fee < r_max * 100)
        except:
            pass
        if index == '1':
            datas = datas.order_by(Requirment.wanna_fee.desc())
        else:
            datas = datas.order_by(Requirment.wanna_fee.asc())


    if requirment_id == 2:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state == 2)
    if requirment_id == 3:
        datas = g.db.query(SuccessRequirment).filter(SuccessRequirment.merchant_id == mc_user.id)
    if requirment_id == 4:
        datas = g.db.query(Requirment).filter(Requirment.merchant_id == mc_user.id, Requirment.state == 4)
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
    url = 'decide_item/%s' % requirment_id
    content = u'商家%s回应了你的发布' % rec.merchant.name
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


@mc.route("/requirment/cancel/<requirment_id>", methods=["GET", "POST"])
def requirment_cancel(requirment_id):
    import random
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    requirment_id = int(requirment_id)
    rec = g.db.query(Requirment).filter(Requirment.id == requirment_id, Requirment.merchant_id == mc_user.id).first()
    if rec and rec.state == 2:
        rec.state = 4
        g.db.add(rec)
        g.db.commit()
        add_success(u'取消交易成功')
    return redirect('/mc/requirment/2')



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
    my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id)
    my_subcatalogs = [rec.catalog for rec in my_subcatalogs]
    return render_template("mc/catalog.html", **locals())

@mc.route("/product/add_catalog", methods=["GET", "POST"])
def add_catalog():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    catalog_type = request.args.get("type", "").strip()
    if catalog_type:
        catalog = g.db.query(Catalog).filter(Catalog.id == catalog_type, Catalog.status == True).first()
        if catalog:
            subcatalogs = g.db.query(SubCatlog).filter(SubCatlog.catalog_id == catalog.id, SubCatlog.status == True)

    else:
        catalogs = g.db.query(Catalog).filter(Catalog.status == True)

    my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id)
    my_subcatalogs = [rec.catalog for rec in my_subcatalogs]
    if request.method == 'POST':
        subcatalogs = request.form.getlist('subcatalog')
        for i, catalog_id in enumerate(subcatalogs):
            if not g.db.query(CustomerCataog).filter(CustomerCataog.catalog_id == catalog_id, CustomerCataog.merchant_id == mc_user.id).first():
                add_sub = CustomerCataog(catalog_id=catalog_id, merchant_id=mc_user.id)
                g.db.add(add_sub)
        g.db.commit()
        add_success(u'添加服务成功')
        return redirect('/mc/product/catalog')
    return render_template("mc/add_catalog.html", **locals())

@mc.route("/product/cancel/<catalog_id>", methods=["GET", "POST"])
def mc_product_cancel(catalog_id):
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    data = g.db.query(CustomerCataog).filter(CustomerCataog.catalog_id == catalog_id, CustomerCataog.merchant_id == mc_user.id).first()
    if data:
        g.db.delete(data)
        g.db.commit()
        add_success(u'成功删除服务')
    return redirect('/mc/product/catalog')

@mc.route("/product/product", methods=["GET", "POST"])
def mc_product():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    datas = g.db.query(Product).filter(Product.merchant_id == mc_user.id, Product.status == True).order_by(Product.id.desc())
    return render_template("mc/product_list.html", **locals())


@mc.route("/product/del/<product_id>", methods=["GET", "POST"])
def mc_product_del(product_id):
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    data = g.db.query(Product).filter(Product.merchant_id == mc_user.id, Product.id == product_id).first()
    if data:
        data.status = False
        g.db.add(data)
        g.db.commit()
        add_success(u'删除商品成功')
        return redirect('/mc/product/product')
    return redirect('/mc/product/product')

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@mc.route("/product/add", methods=["GET", "POST"])
def mc_add_product():
    from admin.views import update_img_by
    from settings import UPLOAD_FOLDER, SITE_ROOT
    import os
    if not g.mc_user:
        return redirect('/mc/login')
    catalogs = g.db.query(Catalog).filter(Catalog.status == True)
    mc_user = g.mc_user
    my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id)
    if request.method == 'POST':
        catalog_id = request.form.get("catalog_id", "0")
        title = request.form.get("title", "")
        descrip = request.form.get("descrip", "")
        show_fee = request.form.get("show_fee", "")
        acept_fee = request.form.get("acept_fee", "")
        try:
            show_fee_init = float(show_fee) * 100
            acept_fee_init = float(acept_fee) * 100
        except:
            add_error(u'显示价格或者最低卖价只能输入数字')
        else:
            if not title or not descrip:
                add_error(u'标题或者介绍不能为空')
            else:
                icon_smaill = request.files.get("icon_smaill", "")
                icon_smaill = update_img_by(icon_smaill,200,120)
                
                icon_large = request.files.get("icon_large", "")
                icon_large = update_img_by(icon_large,640,400)
                
                if not icon_smaill or not icon_large:
                    add_error(u'介绍图 或者列表图 不能为空')
                else:
                    pr = Product(catalog_id=catalog_id, merchant_id=mc_user.id, title=title, descrip=descrip,
                            acept_fee=acept_fee_init, show_fee=show_fee_init, icon_smaill=icon_smaill,
                            icon_large=icon_large, view_count=0, success_count=0
                            )

                    g.db.add(pr)
                    g.db.commit()
                    add_success(u'添加商品成功')
                return redirect('/mc/product/add')

    return render_template("mc/add.html", **locals())

@mc.route("/update_img", methods=["GET", "POST"])
def update_img():
    from settings import UPLOAD_FOLDER
    from werkzeug import secure_filename
    import os
    import datetime
    icon_large = request.files.get("temp_img", "")
    if not icon_large:
        icon_large = request.files.get("Filedata", "")
    
    filename = secure_filename(icon_large.filename)
    filename = str(time.time()).replace('.', '') + '.' + filename.rsplit('.', 1)[1]
    icon_large_filename = filename
    icon_large.seek(0)
    ext = ''
    if g.mc_user:
        ext = 'm%s' % g.mc_user.id
    if g.admin_user:
        ext = 'a%s' % g.admin_user.id
    if not ext:
        ext = datetime.datetime.now().date().isoformat()
    path = os.path.join(UPLOAD_FOLDER, ext)
    if not os.path.exists(path):
        os.makedirs(path)

    icon_large.save(os.path.join(path, icon_large_filename))
    icon_large_src = '/static/upload/%s/%s' % (ext, icon_large_filename)
    if request.files.get("Filedata", ""):
        return icon_large_src
    result = {'succeed':True, 'erro':'%s' % icon_large_src }
    return jsonify(result)


@mc.route("/pre_payed/help", methods=["GET", "POST"])
def pre_payed_help():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    datas = g.db.query(MerchantPayed).filter(MerchantPayed.merchant_id == mc_user.id, MerchantPayed.state == True)
    return render_template("mc/payed.html", **locals())



@mc.route("/pre_payed/pre_payed_list", methods=["GET", "POST"])
def pre_payed_list():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    datas = g.db.query(MerchantPayed).filter(MerchantPayed.merchant_id == mc_user.id, MerchantPayed.state == True)
    return render_template("mc/pre_payed_list.html", **locals())



@mc.route("/pay", methods=["GET", "POST"])
def pay():
    if not g.mc_user:
        return redirect('/mc/login')
    else:
        import alipay
        mc_user = g.mc_user
        order_id = 'BBGJ_%s_%s' % (mc_user.id, str(time.time()).replace('.', ''))
        pre_payed = float(request.args.get("total", "0.01").strip())
        mp = MerchantPayed(order_id=order_id, merchant_id=mc_user.id, pre_payed=pre_payed * 100)
        g.db.add(mp)
        g.db.commit()
        o_alipay = alipay.Alipay()
        alipay_url = o_alipay.create_order_alipay_url(alipay.consumer_subject, order_id, '%.2f' % pre_payed, body=alipay.consumer_body)
        return redirect(alipay_url)

def pay_callback(order_id, total_fee=0):
    from datetime import datetime
    mp = g.db.query(MerchantPayed).filter(MerchantPayed.order_id == order_id).first()
    if mp and not mp.state and mp.pre_payed == int(total_fee * 100):
        mp.state = True
        mp.last_modify = datetime.now()
        g.db.add(mp)
        g.db.commit()
        merchant = mp.merchant
        merchant.pre_payed += int(total_fee * 100)
        g.db.add(merchant)
        g.db.commit()
        return True, ''
    return False, ''



@mc.route("/alipaycallback", methods=["GET", "POST"])
def alipaycallback():
    payState = 'fail'
    payTxt = u'支付遇到问题'
    import alipay
    o_alipay = alipay.Alipay()
    valid, infos = o_alipay.validate(request)
    if valid:
        trade_status = infos['trade_status']
        if trade_status == u'TRADE_FINISHED' or trade_status == u'TRADE_SUCCESS':
            buyer_email = infos['buyer_email']
            buyer_id = infos['buyer_id']
            trade_no = infos['trade_no']
            order_id = infos['out_trade_no']
            total_fee = float(infos['total_fee'])

            try:
                flag, result = pay_callback(order_id, total_fee=total_fee)
                if flag:
                    payState = u'success'
                    payTxt = u'支付成功'
                else:
                    payTxt = u'支付失败'

            except Exception, e:
                payState = u'fail'
                payTxt = u'支付遇到问题: %s' % str(e)

    return render_template("mc/pre_payed_complete.html", **locals())


@mc.route("/alipaynotify", methods=["GET", "POST"])
def alipaynotify():
    payState = u'success'
    import alipay
    o_alipay = alipay.Alipay()
    valid, infos = o_alipay.validate(request)
    if valid:
        trade_status = infos['trade_status']
        if trade_status == u'TRADE_FINISHED' or trade_status == u'TRADE_SUCCESS':
            buyer_email = infos['buyer_email']
            buyer_id = infos['buyer_id']
            trade_no = infos['trade_no']
            order_id = infos['out_trade_no']
            total_fee = float(infos['total_fee'])

            try:
                flag, result = pay_callback(order_id, total_fee=total_fee)
            except Exception, e:
                logging.error(e)
        return Response(payState)



@mc.route("/self/overview", methods=["GET", "POST"])
def overview():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    if request.method == 'POST':
        new_password = request.form.get("new_password", "")
        password = request.form.get("password", "")
        if len(new_password) < 6:
            add_error(u'新密码不能少于6位')
        elif mc_user.password == password:
            mc_user.password = new_password
            g.db.add(mc_user)
            g.db.commit()
            add_success(u'密码修改成功')
        else:
            add_error(u'旧密码输入错误')
    return render_template("mc/overview.html", **locals())


@mc.route("/self/password", methods=["GET", "POST"])
def up_password():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    if request.method == 'POST':
        new_password = request.form.get("new_password", "")
        password = request.form.get("password", "")
        if len(new_password) < 6:
            add_error(u'新密码不能少于6位')
        elif mc_user.password == password:
            mc_user.password = new_password
            g.db.add(mc_user)
            g.db.commit()
            add_success(u'密码修改成功')
        else:
            add_error(u'旧密码输入错误')
    return render_template("mc/password.html", **locals())

@mc.route("/self/statistics", methods=["GET", "POST"])
def statistics():
    if not g.mc_user:
        return redirect('/mc/login')
    import datetime
    mc_user = g.mc_user
    now = datetime.datetime.now()
    to_day = now.date()
    end_day = to_day - datetime.timedelta(days=30)
    datas = g.db.query(SuccessRequirment).filter(SuccessRequirment.merchant_id == mc_user.id, SuccessRequirment.create_time >= end_day)
    datas_ = {}
    for data in datas:
        k = data.create_time.date().isoformat()
        datas_[k] = datas_.get(k, 0) + data.value
    datas = []
    start_day = end_day
    for i in range(30):
        k = end_day.isoformat()
        datas.append([k, datas_.get(k, 0)])
        end_day += datetime.timedelta(days=1)
    return render_template("mc/statistics.html", **locals())


@mc.route("/help", methods=["GET", "POST"])
def help_me():
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    return render_template("mc/help.html", **locals())





@mc.route("/product/edit/<vid>", methods=["GET", "POST"])
def mc_edit_product(vid):
    from admin.views import update_img_by
    from settings import UPLOAD_FOLDER, SITE_ROOT
    import os
    if not g.mc_user:
        return redirect('/mc/login')
    catalogs = g.db.query(Catalog).filter(Catalog.status == True)
    mc_user = g.mc_user
    my_subcatalogs = g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == mc_user.id)
    
    rec = g.db.query(Product).filter(Product.merchant_id == mc_user.id,Product.id == vid).first()
    if not rec:
        return Response('0')
    
    if request.method == 'POST':
        catalog_id = request.form.get("catalog_id", "0")
        title = request.form.get("title", "")
        descrip = request.form.get("descrip", "")
        show_fee = request.form.get("show_fee", "")
        acept_fee = request.form.get("acept_fee", "")
        try:
            show_fee_init = float(show_fee) * 100
            acept_fee_init = float(acept_fee) * 100
        except:
            add_error(u'显示价格或者最低卖价只能输入数字')
        else:
            if not title or not descrip:
                add_error(u'标题或者介绍不能为空')
            else:
                
                icon_smaill = request.files.get("icon_smaill", "")
                icon_smaill = update_img_by(icon_smaill,200,120)
                
                icon_large = request.files.get("icon_large", "")
                icon_large = update_img_by(icon_large,640,400)
                
                
                rec.catalog_id = catalog_id
                rec.title = title
                rec.descrip = descrip
                rec.show_fee_init = show_fee_init
                rec.acept_fee_init = acept_fee_init
                
                if icon_smaill:
                    rec.icon_smaill = icon_smaill
                if icon_large:
                    rec.icon_large = icon_large
                g.db.add(rec)
                g.db.commit()
                add_success(u'修改成功')
                return redirect('/mc/product/product')

    return render_template("mc/edit_product.html", **locals())

@mc.route("/lackcatalog/<vid>", methods=["GET", "POST"])
def lackcatalog_write(vid):
    from models import LackCatalog
    if not g.mc_user:
        return redirect('/mc/login')
    mc_user = g.mc_user
    
    result = [False,'']
    import json
    if request.method == 'POST':
        name = request.form.get("name", "")
        rec = LackCatalog(merchant_id = mc_user.id,name=name,vtype=vid)
        g.db.add(rec)
        g.db.commit()
        result = [True,'']
    return Response(json.dumps(result))

