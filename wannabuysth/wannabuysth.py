from flask import Flask
from flask.ext.script import Manager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import settings
from utils import print_debug
from models import *


app = Flask(__name__)
manage = Manager(app)
app.config.from_object(settings)

DB=create_engine(settings.DB_URI,encoding = "utf-8",pool_recycle=settings.TIMEOUT,echo=False)
Session = scoped_session(sessionmaker(bind=DB))

@app.route('/')
def hello_world():
    return 'Hello World!'

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
    db=Session()
    db.add(Customer(name="test",password="test",mobile="",publish_count=0,success_count=0,total_payed=0,fee=0,current_fee=0,used_fee=0))
    db.flush()
    db.commit()
    print "done"

if __name__ == '__main__':
    manage.run()
