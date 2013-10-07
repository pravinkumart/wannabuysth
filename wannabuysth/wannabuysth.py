# -*- coding: UTF-8 -*-
from flask import Flask, session, g
from flask.ext.script import Manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import send_file, render_template
from utils import print_debug
from home.views import index
from merchant.views import mc
from models import Customer, Merchant
import settings
from flask import redirect

app = Flask(__name__)
manage = Manager(app)
app.config.from_object(settings)

DB = create_engine(settings.DB_URI, encoding="utf-8", echo=False)

Session = sessionmaker(bind=DB)

app.register_blueprint(index)
app.register_blueprint(mc)


@app.route('/')
def hello_world():
    return redirect('/mc')
#    return render_template("base.html", **locals())

@index.route("static/<file_name>")
def down_file(file_name):
    import os
    file_path = os.path.join(os.path.abspath('./static'), file_name)
    return send_file(file_path, mimetype="applcation/stream", as_attachment=True, attachment_filename=file_name)

@app.route('/state')
def state():
    from flask import jsonify
    result = {'succeed':True}
    return jsonify(result)


@manage.command
def init():
    try:
        from models import Base
        Base.metadata.create_all(bind=DB)
    except Exception, e:
        print print_debug(e)
    print "done"

@manage.command
def test():
    db = Session()
    db.add(Customer(name="test", password="test", mobile="", publish_count=0, success_count=0, total_payed=0, fee=0, current_fee=0, used_fee=0))
    db.flush()
    db.commit()
    print "done"

@app.before_request
def before_request():
    """
    """
    g.db = Session()
    #用户登陆信息加载
    user_id = session.get('user_id', None)
    if not user_id:
        g.user = None
    else:
        g.user = g.db.query(Customer).filter(Customer.id == user_id).first()
    #mc 用户登录
    mc_user_id = session.get('mc_user_id', None)
    if not mc_user_id:
        g.mc_user = None
    else:
        g.mc_user = g.db.query(Merchant).filter(Merchant.id == mc_user_id).first()


@app.teardown_request
def tear_down(exception=None):
    """
    当请求结束的时候执行
    """
    if exception:
        print exception
    try:
        if exception:
            g.db.rollback()
        else:
            g.db.commit()
        g.db.close()
    except Exception, e:
        print e


if __name__ == '__main__':
    manage.run()
