#-*- coding:utf-8 -*-
__author__ = 'Alexander'
import datetime
from sqlalchemy import Column,Integer,String,DateTime,Boolean,Text,UniqueConstraint,Table, MetaData,ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship,backref
from decimal import Decimal
 
 
TABLEARGS = {
    'mysql_engine': 'InnoDB',
    'mysql_charset':'utf8'
}
 
class DeclaredBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id =  Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.datetime.now, index=True)
    last_modify = Column(DateTime, default=datetime.datetime.now, index=True)
    status = Column(Boolean,default=True)
 
Base = declarative_base(cls=DeclaredBase)

class Catalog(Base):
    name = Column(String(100))        #频道名
    descp = Column(String(500))       #频道说明
    icon_smaill = Column(String(200)) #小图标
    icon_large = Column(String(200))  #大图标

class SubCataog(Base):
    catalog_id = Column(Integer,ForeignKey("catalog.id")) #父级频道编号
    catalog = relationship("Catalog.id")                  #父级频道对象
    name = Column(100)                                    #分类名
    descp = Column(500)                                   #分类介绍
    icon_smaill = Column(String(200))                     #小图标
    icon_large = Column(String(200))                      #大图标



class Customer(Base):
    name = Column(String(20), unique=True)       #消费者名
    password = Column(String(48))                #密码
    mobile = Column(String(11))                  #手机号
    publish_count = Column(Integer)              #发布需求总数
    success_count = Column(Integer)              #成功需求总数
    total_payed = Column(Integer)                #总金额
    fee = Column(Integer)                        #消费基金总数
    current_fee = Column(Integer)                #消费基金余额
    used_fee = Column(Integer)                   #使用金额

class Merchant(Base):
    name = Column(String(20), unique=True)       #商家名
    password = Column(String(48))                #密码
    mobile = Column(String(11))                  #手机号
    pre_payed = Column(Integer)                  #预付款总额
    credit = Column(Integer)                     #信誉度
    success_count = Column(Integer)              #成功次数
    faild_count = Column(Integer)                #失败次数
