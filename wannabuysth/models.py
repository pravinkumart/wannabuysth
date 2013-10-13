# -*- coding:utf-8 -*-
__author__ = 'Alexander'
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import Text, UniqueConstraint, ForeignKey, SmallInteger, Index
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import relationship, backref


class DeclaredBase(object):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime, default=datetime.datetime.now, index=True)
    last_modify = Column(DateTime, default=datetime.datetime.now, index=True)
    status = Column(Boolean, default=True)

Base = declarative_base(cls=DeclaredBase)

#-------------------上面的是基类，不要动---------------------------------

class Catalog(Base):
    """
    频道
    """
    name = Column(String(100), unique=True)  # 频道名
    descp = Column(String(500))  # 频道说明
    icon_smaill = Column(String(200))  # 小图标
    icon_large = Column(String(200))  # 大图标
    idx = Column(SmallInteger)  # 排序

class SubCataog(Base):
    """
    子目录
    """
    catalog_id = Column(Integer, ForeignKey("catalog.id"))  # 父级频道编号
    catalog = relationship("Catalog", backref=backref("subcatalogs"))  # 父级频道对象
    name = Column(String(100), unique=True)  # 分类名
    pingying = Column(String(100))  # 分类名
    descp = Column(String(500))  # 分类介绍
    icon_smaill = Column(String(200))  # 小图标
    icon_large = Column(String(200))  # 大图标
    idx = Column(SmallInteger)  # 排序
    count = Column(Integer, default=0)  # 总金额

    def get_img(self):
        if self.icon_smaill:
            return self.icon_smaill
        else:
            return '/static/data/type.jpg'



class Customer(Base):
    """
    @note: 用户
    """
    name = Column(String(20), unique=True)  # 消费者名
    password = Column(String(48))  # 密码
    mobile = Column(String(11), unique=True)  # 手机号
    publish_count = Column(Integer)  # 发布需求总数
    success_count = Column(Integer)  # 成功需求总数
    total_payed = Column(Integer)  # 总金额
    used_fee = Column(Integer)  # 使用金额
    fee = Column(Integer)  # 消费基金总数(单位：分)
    current_fee = Column(Integer)  # 消费基金余额(单位：分)
    user_level = Column(Integer, default=0)  # 用户等级
    vip_end_time = Column(DateTime)  # 会员到期时间
    portrait = Column(Text)  # 头像
    state = Column(Boolean, default=True)

    def get_name(self):
        try:
            int(self.name)
            return u'新用户'
        except:
            return self.name

    def get_user_level(self):
        x = [0 for i in  range(5)]
        for i in range(self.user_level):
            if i > 4:
                break
            x[i] = 1
        return x

    def get_vip(self):
        if self.vip_end_time:
            return 1
        else:
            return 0

    def get_portrait(self):
        if self.portrait:
            return 'data:image/jpeg;base64,%s' % self.portrait
        else:
            return '/static/data/my_portrait.png'


class CustomerCataog(Base):
    """
    @note: 用户选择的类别
    """
    catalog_id = Column(Integer, ForeignKey("subcataog.id"))
    catalog = relationship("SubCataog")

    merchant_id = Column(Integer, ForeignKey("merchant.id"))
    merchant = relationship("Merchant")



class Merchant(Base):
    """
    商家
    """
    name = Column(String(20), unique=True)  # 商家名
    password = Column(String(48))  # 密码
    mobile = Column(String(11))  # 手机号
    pre_payed = Column(Integer)  # 预付款总额 (单位：分)
    credit = Column(Integer)  # 信誉度
    success_count = Column(Integer)  # 成功次数
    faild_count = Column(Integer)  # 失败次数
    catalog_count = Column(Integer, default=1)  # 限制服务大类 数量
    subcatalog_count = Column(Integer, default=3)  # 限制服务小类 数量


class Product(Base):
    """
    商家发布的商品或者服务
    """
    catalog_id = Column(Integer, ForeignKey("subcataog.id"))  # 父级频道编号
    catalog = relationship("SubCataog", backref=backref("products"))  # 父级频道对象
    merchant_id = Column(Integer, ForeignKey("merchant.id"))  # 商家ID
    merchant = relationship("Merchant", backref=backref("replys"))  # 商家对象
    title = Column(String(30))
    descrip = Column(String(500))  # 商品
    acept_fee = Column(Integer)  # 最低接收价格
    show_fee = Column(Integer)  # 显示价格
    icon_smaill = Column(String(200))  # 小图标
    icon_large = Column(String(200))  # 大图标
    view_count = Column(Integer)  # 浏览次数
    success_count = Column(Integer)  # 成功次数

    def get_show_fee(self):
        return self.show_fee

class ProductAds(Base):
    '''
    @note: 产品广告
    '''
    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", backref=backref("ads"))  # 商品或者服务
    start_time = Column(DateTime)  # 开始时间
    end_time = Column(DateTime)  # 结束时间
    img = Column(String(200))  # 广告图片
    type = Column(Integer)  # 广告类型 0 首页广告，1 广告列表中的第一张   2 广告列表里面的小广告
    sort_num = Column(Integer)  # 排序 字段 越大越靠钱




class Requirment(Base):
    """
    消费者发布的需求
    """
    customer_id = Column(Integer, ForeignKey("customer.id"))  # 消费者编号
    customer = relationship("Customer", backref=backref("requirments"))  # 消费者

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", backref=backref("reqs"))  # 商品或者服务

    subcataog_id = Column(Integer, ForeignKey("subcataog.id"))
    subcataog = relationship("SubCataog", backref=backref("requirments"))

    merchant_id = Column(Integer, ForeignKey("merchant.id"))  # 中标商家ID
    merchant = relationship("Merchant", backref=backref("requirments"))

    reply_id = Column(Integer)  # 中标回复


    wanna_fee = Column(Integer)  # 心理价位 (单位：分)
    descrip = Column(String(500))  # 需求描述
    end_time = Column(DateTime)  # 截止时间
    location = Column(String(200))  # 服务地点
    code = Column(String(6))  # 交易码
    state = Column(SmallInteger)
    __table_args__ = (
        Index("customer_requirment_idx", "customer_id", "state"),
    )

    def get_wanna_fee(self):
        return self.wanna_fee / 100.0

    def get_state(self):
        return {0:u'用户新发布 ', 1:u'用户选定商家 ', 2:u'商家确定 ', 3:u'交易完成', 4:u'交易失败'}.get(self.state, self.state)




class Reply(Base):
    """
    商家回复需求应标
    """
    requirment_id = Column(Integer, ForeignKey("requirment.id"))  # 需求编号
    requirment = relationship("Requirment", backref=backref("replys"))  # 需求对象

    merchant_id = Column(Integer, ForeignKey("merchant.id"))  # 回复商家ID
    merchant = relationship("Merchant")  # 回复商家对象
    fee = Column(Integer)  # 服务价格 (单位：分)
    descrip = Column(String(500))  # 服务描述
    __table_args__ = (
        Index("merchant_reply_idx", "requirment_id", "merchant_id"),
    )

    def get_fee(self):
        return self.fee / 100.0

class SuccessRequirment(Base):
    """
    成功的需求单独备份
    """
    customer_id = Column(Integer, ForeignKey("customer.id"))  # 消费者编号
    customer = relationship("Customer", backref=backref("success_requirments"))  # 消费者

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product", backref=backref("success_reqs"))  # 商品或者服务

    subcataog_id = Column(Integer, ForeignKey("subcataog.id"))
    subcataog = relationship("SubCataog", backref=backref("success_requirments"))

    merchant_id = Column(Integer, ForeignKey("merchant.id"))  # 中标商家ID
    merchant = relationship("Merchant", backref=backref("success_requirments"))

    wanna_fee = Column(Integer)  # 成交价格
    descrip = Column(String(500))  # 需求描述
    end_time = Column(DateTime)  # 截止时间
    location = Column(String(200))  # 服务地点
    succes_fee = Column(Integer)  # 成交价位 (单位：分)
    state = Column(SmallInteger)
    reply_id = Column(Integer, ForeignKey("reply.id"))  # 中标回复
    reply = relationship("Reply", backref=backref("successrequirment"))


class ShowCase(Base):
    """
    秀单帖
    """
    show_type = Column(SmallInteger)  # 秀单帖类型 0比低 1比高
    requirment_id = Column(Integer, ForeignKey("successrequirment.id"))  # 需求编号
    requirment = relationship("SuccessRequirment", backref=backref("showcase", uselist=False))  # 需求对象
    customer_id = Column(Integer, ForeignKey("customer.id"))  # 消费者编号
    customer = relationship("Customer")  # 消费者
    wanna_fee = Column(Integer)  # 成交价格

    def get_wanna_fee(self):
        return self.wanna_fee / 100.0

class ShowCaseReplay(Base):
    """
    跟帖
    """
    showcase_id = Column(Integer, ForeignKey("showcase.id"))
    showcase = relationship("ShowCase", backref=backref("replys"))
    requirment_id = Column(Integer, ForeignKey("successrequirment.id"))  # 需求编号
    requirment = relationship("SuccessRequirment")  # 需求对象
    customer_id = Column(Integer, ForeignKey("customer.id"))  # 消费者编号
    customer = relationship("Customer")  # 消费者
    wanna_fee = Column(Integer)  # 成交价格

    def get_wanna_fee(self):
        return self.wanna_fee / 100.0

class Comments(Base):
    '''
    @note: 评论
    '''
    showcase_id = Column(Integer, ForeignKey("showcase.id"))
    showcase = relationship("ShowCase")

    customer_id = Column(Integer, ForeignKey("customer.id"))  # 消费者编号
    customer = relationship("Customer")  # 消费者

    content = Column(Text)  # 评论内容

    def get_wanna_fee(self):
        return self.wanna_fee / 100.0




class UserExternalBind(Base):
    '''
    @站外绑定表
    '''
    access_token = Column(String(100))
    refresh_token = Column(String(100))
    external_user_id = Column(String(100))
    source = Column(String(100))
    catalog = Column(String(100))

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")


class Notification(Base):
    '''
    @note: 系统通知
    '''

    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship("Customer")

    content = Column(Text)  # 评论内容
    type = Column(Integer)  # 类型   0系统消息   1回应
    url = Column(Text)  # 连接地址
    is_visit = Column(Boolean, default=False)


