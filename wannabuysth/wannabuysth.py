from flask import Flask
from flask.ext.script import Manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import settings
from utils import print_debug
from models import *
from home.views import index

app = Flask(__name__)
manage = Manager(app)
app.config.from_object(settings)

DB = create_engine(settings.DB_URI, encoding="utf-8", pool_recycle=settings.TIMEOUT, echo=False)
Session = scoped_session(sessionmaker(bind=DB))

app.register_blueprint(index)
from flask import send_file, render_template

@app.route('/')
def hello_world():
    return render_template("base.html", **locals())

@index.route("static/<file_name>")
def down_file(file_name):
    import os
    file_path = os.path.join(os.path.abspath('./static'), file_name)
    return send_file(file_path, mimetype="applcation/stream", as_attachment=True, attachment_filename=file_name)

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

if __name__ == '__main__':
    manage.run()
