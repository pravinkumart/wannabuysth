# -*- coding: UTF-8 -*-
import logging
from flask import Blueprint, render_template, abort, g, request, Response
from flask import redirect, url_for, session, flash, send_file
from flask import jsonify
import time
from models import AdminUser, Statistics
from datetime import datetime
from utils import add_error, add_success
from models import Catalog, SubCatlog
from sqlalchemy import or_
from models import Product, Merchant, Requirment
from models import ProductAds

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
        if request.method == 'POST':
            new_password = request.form.get("new_password", "")
            password = request.form.get("password", "")
            if len(new_password) < 6:
                add_error(u'新密码不能少于6位')
            elif admin_user.password == password:
                admin_user.password = new_password
                g.db.add(admin_user)
                g.db.commit()
                add_success(u'密码修改成功')
            else:
                add_error(u'旧密码输入错误')
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
                add_error(u'帐号或密码错误')
    return render_template("admin/login.html", **locals())


@admin.route("/logout", methods=["GET", "POST"])
def admin_logout():
    session["mc_user_id"] = ''
    return redirect('/admin/login')

def update_img_by(icon_large, width=None, height=None):
    from PIL import Image, ImageEnhance
    from settings import UPLOAD_FOLDER
    from merchant.image_thumbnail import resize_img
    import os
    import random
    if not icon_large:
        return ''
    filename = str(time.time()).replace('.', '') + str(random.randint(10, 100)) + '.png'
    icon_large_filename = filename
    icon_large.seek(0)
    ext = ''
    if g.mc_user:
        ext = 'm%s' % g.mc_user.id
    if g.admin_user:
        ext = 'a%s' % g.admin_user.id
    path = os.path.join(UPLOAD_FOLDER, ext)
    if not os.path.exists(path):
        os.makedirs(path)
    if width and height:
        try:
            icon_large = Image.open(icon_large)
        except:
            return ''
        icon_large = resize_img(icon_large, width, height)
    icon_large.save(os.path.join(path, icon_large_filename))
    icon_large_src = '/static/upload/%s/%s' % (ext, icon_large_filename)
    return icon_large_src

@admin.route("/catalog", methods=["GET", "POST"])
@admin.route("/catalog/<vid>/update", methods=["GET", "POST"])
def catalog(vid=0):
    if not g.admin_user:
        return redirect('/admin/login')
    cu_catalog = int(request.args.get("catalog", "0"))
    admin_user = g.admin_user
    if vid != 0:
        catalog = g.db.query(Catalog).filter(Catalog.id == vid).first()
    else:
        catalog = None

    if request.method == 'POST':
        name = request.form.get("name", "")
        descp = request.form.get("descp", "")
#         icon_smaill = request.form.get("icon_smaill", "")
#         icon_large = request.form.get("icon_large", "")
        idx = request.form.get("idx", "0")
        
        icon_smaill = request.files.get("icon_smaill", "")
        icon_smaill = update_img_by(icon_smaill)
        
        icon_large = request.files.get("icon_large", "")
        icon_large = update_img_by(icon_large)

        if vid == 0:
            if g.db.query(Catalog).filter(Catalog.name == name).first():
                add_error(u'频道名字已存在')
            else:
                c = Catalog(name=name, descp=descp, icon_smaill=icon_smaill, icon_large=icon_large, idx=idx)
                g.db.add(c)
                g.db.commit()
                add_success(u'频道添加成功')
                return redirect('/admin/catalog?catalog=%s' % c.id)
        else:
            if g.db.query(Catalog).filter(Catalog.name == name, Catalog.id != vid).first():
                add_error(u'频道名字已存在')
            else:
                catalog.name = name
                catalog.descp = descp
                if icon_smaill:
                    catalog.icon_smaill = icon_smaill
                if icon_large:
                    catalog.icon_large = icon_large
                catalog.idx = idx
                g.db.add(catalog)
                g.db.commit()
                add_success(u'频道修改成功')
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
#         icon_smaill = request.form.get("icon_smaill", "")
#         icon_large = request.form.get("icon_large", "")
        idx = request.form.get("idx", "0")
        pingying = request.form.get("pingying", "")
        
        icon_smaill = request.files.get("icon_smaill", "")
        icon_smaill = update_img_by(icon_smaill)
        
        icon_large = request.files.get("icon_large", "")
        icon_large = update_img_by(icon_large)
        
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


@admin.route("/subcatlog/<vid>/update", methods=["GET", "POST"])
def sub_catalog_edit(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    catalogs = g.db.query(Catalog).all()
    sub_catalog = g.db.query(SubCatlog).filter(SubCatlog.id == vid).first()
    cu_catalog = sub_catalog.catalog_id
    if request.method == 'POST':
        name = request.form.get("name", "")
        descp = request.form.get("descp", "")
#         icon_smaill = request.form.get("icon_smaill", "")
#         icon_large = request.form.get("icon_large", "")
        idx = request.form.get("idx", "0")
        pingying = request.form.get("pingying", "")
        
        icon_smaill = request.files.get("icon_smaill", "")
        icon_smaill = update_img_by(icon_smaill)
        
        icon_large = request.files.get("icon_large", "")
        icon_large = update_img_by(icon_large)

        if not name:
            add_error(u'名字不能为空')
        else:
            if g.db.query(SubCatlog).filter(SubCatlog.name == name, SubCatlog.id != sub_catalog.id).first():
                add_error(u'频道名字已存在')
            else:
                sub_catalog.name = name
                sub_catalog.descp = descp
                sub_catalog.pingying = pingying
                if icon_smaill:
                    sub_catalog.icon_smaill = icon_smaill
                if icon_large:
                    sub_catalog.icon_large = icon_large
                g.db.add(sub_catalog)
                g.db.commit()
                add_success(u'修改成功')
                return redirect('/admin/catalog?catalog=%s' % sub_catalog.catalog_id)
    return render_template("admin/sub_catalog_edit.html", **locals())

@admin.route("/mc_user", methods=["GET", "POST"])
def mc_user():
    if not g.admin_user:
        return redirect('/admin/login')
    name = request.args.get("name", "").strip()
    admin_user = g.admin_user
    datas = g.db.query(Merchant).order_by(Merchant.id)
    if name:
        datas = datas.filter(or_(Merchant.name.ilike('%%%s%%' % name), Merchant.mobile.ilike('%%%s%%' % name)))
    return render_template("admin/mc_user.html", **locals())

@admin.route("/mc_user/<vid>/del", methods=["GET", "POST"])
def mc_user_del(vid):
    from models import CustomerCataog, Reply
    from models import MerchantPayed, SuccessRequirment
    if not g.admin_user or not g.admin_user.is_admin():
        return redirect('/admin/login')
    data = g.db.query(Merchant).filter(Merchant.id == vid).first()
    for d in g.db.query(CustomerCataog).filter(CustomerCataog.merchant_id == vid):
        g.db.delete(d)
    for d in g.db.query(MerchantPayed).filter(MerchantPayed.merchant_id == vid):
        g.db.delete(d)
    for d in g.db.query(Product).filter(Product.merchant_id == vid):
        g.db.delete(d)
    for d in g.db.query(SuccessRequirment).filter(SuccessRequirment.merchant_id == vid):
        g.db.delete(d)
    for d in g.db.query(Reply).filter(Reply.merchant_id == vid):
        g.db.delete(d)
    for d in g.db.query(Requirment).filter(Requirment.merchant_id == vid):
        g.db.delete(d)
    g.db.delete(data)
    g.db.commit()
    add_success(u'删除成功')
    return redirect('/admin/mc_user')

@admin.route("/mc_user/<vid>/disable", methods=["GET", "POST"])
def mc_user_disable(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    data = g.db.query(Merchant).filter(Merchant.id == vid).first()
    data.status = False
    g.db.add(data)
    g.db.commit()
    add_success(u'成功禁止')
    return redirect('/admin/mc_user')


@admin.route("/mc_user/<vid>/able", methods=["GET", "POST"])
def mc_user_able(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    data = g.db.query(Merchant).filter(Merchant.id == vid).first()
    data.status = True
    g.db.add(data)
    g.db.commit()
    add_success(u'成功开启')
    return redirect('/admin/mc_user')

@admin.route("/mc_user/<vid>/up_password", methods=["GET", "POST"])
def mc_user_up_password(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    password = request.form.get("password", "")
    if len(password) < 6:
        add_error(u'密码不能少于6位')
        return redirect('/admin/mc_user')
    data = g.db.query(Merchant).filter(Merchant.id == vid).first()
    data.password = password
    g.db.add(data)
    g.db.commit()
    add_success(u'密码修改成功')
    return redirect('/admin/mc_user')

@admin.route("/cu_user/<vid>/up_password", methods=["GET", "POST"])
def cu_user_up_password(vid):
    from models import Customer
    if not g.admin_user:
        return redirect('/admin/login')
    password = request.form.get("password", "")
    if len(password) < 6:
        add_error(u'密码不能少于6位')
        return redirect('/admin/cu_user')
    data = g.db.query(Customer).filter(Customer.id == vid).first()
    data.password = password
    g.db.add(data)
    g.db.commit()
    add_success(u'密码修改成功')
    return redirect('/admin/cu_user')

@admin.route("/cu_user", methods=["GET", "POST"])
def cu_user():
    if not g.admin_user:
        return redirect('/admin/login')
    from models import Customer
    name = request.args.get("name", "").strip()
    admin_user = g.admin_user
    datas = g.db.query(Customer).order_by(Customer.id)
    if name:
        datas = datas.filter(or_(Customer.name.ilike('%%%s%%' % name), Customer.mobile.ilike('%%%s%%' % name)))
    return render_template("admin/cu_user.html", **locals())


@admin.route("/cu_user/<vid>/del", methods=["GET", "POST"])
def cu_user_del(vid):
    from models import Customer, Comments, Notification, Requirment
    from models import SuccessRequirment, ShowCase, ShowCaseReplay
    if not g.admin_user or not g.admin_user.is_admin():
        return redirect('/admin/login')

    data = g.db.query(Customer).filter(Customer.id == vid).first()
    for d in g.db.query(Comments).filter(Comments.customer_id == vid):
        g.db.delete(d)
    for d in g.db.query(Notification).filter(Notification.customer_id == vid):
        g.db.delete(d)
    for d in g.db.query(ShowCase).filter(ShowCase.customer_id == vid):
        g.db.delete(d)
    for d in g.db.query(Requirment).filter(Requirment.customer_id == vid):
        g.db.delete(d)
    for d in g.db.query(ShowCaseReplay).filter(ShowCaseReplay.customer_id == vid):
        g.db.delete(d)
    for d in g.db.query(SuccessRequirment).filter(SuccessRequirment.customer_id == vid):
        g.db.delete(d)
    g.db.delete(data)
    g.db.commit()
    add_success(u'删除成功')
    return redirect('/admin/cu_user')


@admin.route("/cu_user/<vid>/disable", methods=["GET", "POST"])
def cu_user_disable(vid):
    from models import Customer
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    data = g.db.query(Customer).filter(Customer.id == vid).first()
    data.status = False
    g.db.add(data)
    g.db.commit()
    add_success(u'成功禁止')
    return redirect('/admin/cu_user')


@admin.route("/cu_user/<vid>/able", methods=["GET", "POST"])
def cu_user_able(vid):
    from models import Customer
    if not g.admin_user:
        return redirect('/admin/login')
    data = g.db.query(Customer).filter(Customer.id == vid).first()
    data.status = True
    g.db.add(data)
    g.db.commit()
    add_success(u'成功开启')
    return redirect('/admin/cu_user')


@admin.route("/statistics", methods=["GET", "POST"])
def statistics():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        return render_template("admin/index.html", **locals())


@admin.route("/statistics/mc", methods=["GET", "POST"])
def statistics_mc():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        now = datetime.now()
        start_day = datetime(now.year, 1, 1)
        end_day = datetime(now.year, 12, 31)
        datas = g.db.query(Statistics).filter(Statistics.type == 0, Statistics.cur_day >= start_day, Statistics.cur_day <= end_day)
        datas_ = {}
        for data in datas:
            datas_[data.cur_day.date().isoformat()] = data.value
        datas = []
        for i in range(12):
            k = '%s-%02d-01' % (now.year, i + 1)
            datas.append([k, datas_.get(k, 0)])
        return render_template("admin/statistics_mc.html", **locals())



@admin.route("/statistics/cu", methods=["GET", "POST"])
def statistics_cu():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        now = datetime.now()
        start_day = datetime(now.year, 1, 1)
        end_day = datetime(now.year, 12, 31)
        datas = g.db.query(Statistics).filter(Statistics.type == 1, Statistics.cur_day >= start_day, Statistics.cur_day <= end_day)
        datas_ = {}
        for data in datas:
            datas_[data.cur_day.date().isoformat()] = data.value
        datas = []
        for i in range(12):
            k = '%s-%02d-01' % (now.year, i + 1)
            datas.append([k, datas_.get(k, 0)])
        return render_template("admin/statistics_cu.html", **locals())


@admin.route("/statistics/su", methods=["GET", "POST"])
def statistics_su():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        now = datetime.now()
        start_day = datetime(now.year, 1, 1)
        end_day = datetime(now.year, 12, 31)
        datas = g.db.query(Statistics).filter(Statistics.type == 2, Statistics.cur_day >= start_day, Statistics.cur_day <= end_day)
        datas_ = {}
        for data in datas:
            datas_[data.cur_day.date().isoformat()] = data.value
        datas = []
        for i in range(12):
            k = '%s-%02d-01' % (now.year, i + 1)
            datas.append([k, datas_.get(k, 0)])
        return render_template("admin/statistics_su.html", **locals())



@admin.route("/admin_user", methods=["GET", "POST"])
def admin_user():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        datas = g.db.query(AdminUser).filter(AdminUser.name != 'admin').order_by(AdminUser.id)
        return render_template("admin/admin_user.html", **locals())


@admin.route("/admin_user/add", methods=["GET", "POST"])
def admin_user_add():
    if not g.admin_user:
        return redirect('/admin/login')
    else:
        admin_user = g.admin_user
        if request.method == 'POST':
            name = request.form.get("name", "")
            mobile = request.form.get("mobile", "")
            password = request.form.get("password", "")

            if not name or not password:
                add_error(u'帐号或密码不能为空')
            else:
                if g.db.query(AdminUser).filter(AdminUser.name == name).first():
                    add_error(u'帐号已存在')
                else:
                    c = AdminUser(name=name, mobile=mobile, password=password)
                    g.db.add(c)
                    g.db.commit()
                    add_success(u'成功添加管理员')
                    return redirect('/admin/admin_user')
        return render_template("admin/admin_add.html", **locals())



@admin.route("/admin_user/<vid>/disable", methods=["GET", "POST"])
def admin_user_disable(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    data = g.db.query(AdminUser).filter(AdminUser.id == vid).first()
    data.status = False
    g.db.add(data)
    g.db.commit()
    add_success(u'成功禁止')
    return redirect('/admin/admin_user')


@admin.route("/admin_user/<vid>/able", methods=["GET", "POST"])
def admin_user_able(vid):
    from models import Customer
    if not g.admin_user:
        return redirect('/admin/login')
    data = g.db.query(AdminUser).filter(AdminUser.id == vid).first()
    data.status = True
    g.db.add(data)
    g.db.commit()
    add_success(u'成功开启')
    return redirect('/admin/admin_user')

@admin.route("/admin_user/<vid>/up_password", methods=["GET", "POST"])
def admin_user_up_password(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    password = request.form.get("password", "")
    if len(password) < 6:
        add_error(u'密码不能少于6位')
        return redirect('/admin/admin_user')
    data = g.db.query(AdminUser).filter(AdminUser.id == vid).first()
    data.password = password
    g.db.add(data)
    g.db.commit()
    add_success(u'密码修改成功')
    return redirect('/admin/admin_user')


@admin.route("/cu_product", methods=["GET", "POST"])
def cu_product():
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    datas = g.db.query(Product).filter(Product.status == True)
    return render_template("admin/product_list.html", **locals())

@admin.route("/requirment", methods=["GET", "POST"])
def requirment():
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    datas = g.db.query(Requirment).order_by(Requirment.id.desc())
    return render_template("admin/requirment.html", **locals())

@admin.route("/lackcatalog/<vid>", methods=["GET", "POST"])
def lackcatalog_show(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    from models import LackCatalog
    datas = g.db.query(LackCatalog).filter(LackCatalog.vtype == vid).order_by(LackCatalog.id.desc())
    return render_template("admin/lackcatalog_list.html", **locals())



@admin.route("/lackcatalog/del/<vid>", methods=["GET", "POST"])
def lackcatalog_del(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    from models import LackCatalog
    rec = g.db.query(LackCatalog).filter(LackCatalog.id == vid).first()
    vtype = rec.vtype 
    g.db.delete(rec)
    g.db.commit()
    add_success(u'删除成功')
    return redirect('/admin/lackcatalog/%s' % vtype)


@admin.route("/notice/<vid>", methods=["GET", "POST"])
def notice_show(vid=0):
    import json
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    from models import Notice
    if request.method == 'POST':
            name = request.form.get("name", "")
            c = Notice(name=name, vtype=vid)
            g.db.add(c)
            g.db.commit()
            return Response(json.dumps([True, '']))
    datas = g.db.query(Notice).filter(Notice.vtype == vid).order_by(Notice.id.desc())
    return render_template("admin/notice_list.html", **locals())


@admin.route("/notice/del/<vid>", methods=["GET", "POST"])
def notice_del(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    from models import Notice
    rec = g.db.query(Notice).filter(Notice.id == vid).first()
    vtype = rec.vtype 
    g.db.delete(rec)
    g.db.commit()
    add_success(u'删除成功')
    return redirect('/admin/notice/%s' % vtype)


@admin.route("/good_product/del/<vid>", methods=["GET", "POST"])
def good_product_del(vid):
    if not g.admin_user:
        return redirect('/admin/login')
    from models import Notice
    rec = g.db.query(ProductAds).filter(ProductAds.id == vid).first()
    g.db.delete(rec)
    g.db.commit()
    add_success(u'删除成功')
    return redirect('/admin/good_product/list')


@admin.route("/good_product/add", methods=["GET", "POST"])
def good_product_add():
    from models import Product
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    mc_id = request.args.get("mc_id", "0")
    mc = g.db.query(Merchant).filter(Merchant.id == mc_id).first()
    if not mc:
        datas = g.db.query(Merchant).order_by(Merchant.id)
        return render_template("admin/good_product_add.html", **locals())
    else:
        datas = g.db.query(Product).filter(Product.merchant_id == mc_id)
        return render_template("admin/good_product_add_2.html", **locals())
    


@admin.route("/good_product/add/<vid>", methods=["GET", "POST"])
def good_product_ok(vid):
    from models import Product
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    product = g.db.query(Product).filter(Product.id == vid).first()
    mc = product.merchant
    if request.method == 'POST':
        start_time = request.form.get("start_time", "")
        end_time = request.form.get("end_time", "")
        sort_num = request.form.get("sort_num", "0")
        vtype = int(request.form.get("type", "1"))
        icon_smaill = request.files.get("img", "")
        if vtype == 0:
            icon_smaill = update_img_by(icon_smaill, 230, 115)
        elif vtype == 1:
            icon_smaill = update_img_by(icon_smaill, 290, 100)
        else:
            icon_smaill = update_img_by(icon_smaill, 135, 100)
            
        if not start_time or not end_time:
            add_error(u'开始或者结束时间不能为空')
        elif not icon_smaill:
            add_error(u'图片不能为空')
        else:
            c = ProductAds(start_time=start_time, end_time=end_time, img=icon_smaill, type=vtype, sort_num=sort_num, product_id=vid)
            g.db.add(c)
            g.db.commit()
            add_success(u'添加成功')
            return redirect('/admin/good_product/add?mc_id=%s' % mc.id)
    return render_template("admin/good_product_add_ok.html", **locals())
    
    


@admin.route("/good_product/list", methods=["GET", "POST"])
def good_product_list():
    from models import Product
    if not g.admin_user:
        return redirect('/admin/login')
    admin_user = g.admin_user
    datas = g.db.query(ProductAds).filter(ProductAds.status == True).order_by(ProductAds.sort_num.desc(), ProductAds.start_time.desc())
    return render_template("admin/good_product_list.html", **locals())


