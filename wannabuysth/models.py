#-*- coding:utf-8 -*-
__author__ = 'Alexander'
import datetime
from sqlalchemy import Column,Integer,String,DateTime,Boolean,Text,UniqueConstraint,Table, MetaData,ForeignKey, SmallInteger
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship,backref
from decimal import Decimal

 
class DeclaredBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id =  Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.datetime.now, index=True)
    last_modify = Column(DateTime, default=datetime.datetime.now, index=True)
    status = Column(Boolean,default=True)
 
Base = declarative_base(cls=DeclaredBase)


#-------------------上面的是基类，不要动---------------------------------



class Catalog(Base):
    """
    频道
    """
    name = Column(String(100))        #频道名
    descp = Column(String(500))       #频道说明
    icon_smaill = Column(String(200)) #小图标
    icon_large = Column(String(200))  #大图标

class SubCataog(Base):
    """
    子目录
    """
    catalog_id = Column(Integer,ForeignKey("catalog.id"))            #父级频道编号
    catalog = relationship("Catalog",backref=backref("subcatalogs")) #父级频道对象
    name = Column(100)                                               #分类名
    descp = Column(500)                                              #分类介绍
    icon_smaill = Column(String(200))                                #小图标
    icon_large = Column(String(200))                                 #大图标



class Customer(Base):
    """
    消费者
    """
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
    """
    商家
    """
    name = Column(String(20), unique=True)       #商家名
    password = Column(String(48))                #密码
    mobile = Column(String(11))                  #手机号
    pre_payed = Column(Integer)                  #预付款总额
    credit = Column(Integer)                     #信誉度
    success_count = Column(Integer)              #成功次数
    faild_count = Column(Integer)                #失败次数


class Product(Base):
    """
    商家发布的商品或者服务
    """
    catalog_id = Column(Integer,ForeignKey("catalog.id"))               #父级频道编号
    catalog = relationship("Catalog",backref=backref("subcatalogs"))    #父级频道对象
    merchant_id = Column(Integer, ForeignKey("merchant.id"))            #商家ID
    merchant = relationship("Merchant",backref=backref("replys"))       #商家对象
    descrip = Column(String(500))                                       #商品
    icon_smaill = Column(String(200)) #小图标
    icon_large = Column(String(200))  #大图标



class Requirment(Base):
    """
    消费者发布的需求
    """
    customer_id = Column(Integer,ForeignKey("customer.id"))             #消费者编号
    customer = relationship("Customer", backref=backref("requirments")) #消费者
    merchant_id = Column(Integer)                                       #中标商家ID
    descrip = Column(String(500))                                       #需求描述
    end_time = Column(DateTime)                                         #截止时间
    location = Column(String(200))                                      #服务地点
    state = Column(SmallInteger)                                        #状态

class Reply(Base):
    """
    商家回复需求应标
    """
    requirment_id = Column(Integer,ForeignKey("requirment.id"))         #需求编号
    requirment = relationship("Requirment",backref=backref("replys"))   #需求对象
    merchant_id = Column(Integer, ForeignKey("merchant.id"))            #回复商家ID
    merchant = relationship("Merchant",backref=backref("replys"))       #回复商家对象
    fee = Column(Integer)                                               #服务价格
    descrip = Column(String(500))                                       #服务描述

class SuccessRequirment(Base):
    """
    成功的需求单独备份
    """
    customer_id = Column(Integer,ForeignKey("customer.id"))             #消费者编号
    customer = relationship("Customer", backref=backref("requirments")) #消费者
    merchant_id = Column(Integer)                                       #中标商家ID
    descrip = Column(String(500))                                       #需求描述
    end_time = Column(DateTime)                                         #截止时间
    location = Column(String(200))                                      #服务地点
    state = Column(SmallInteger)
