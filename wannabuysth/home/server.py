# -*- coding: UTF-8 -*-

from flask import g
from models import Customer

def change_password(username, password):
    '''
    @note: 修改帐号密码
    '''
    user = g.db.query(Customer).filter(Customer.mobile == username).first()
    if user:
        user.password = password
        g.db.add(user)
        g.db.commit()
        return True
    else:
        return False

def update_user_portrait(mobile, image):
    '''
    @note: 修改头像
    '''
    user = g.db.query(Customer).filter(Customer.mobile == mobile).first()
    if user:
        user.portrait = image
        g.db.add(user)
        g.db.commit()
        return True
    else:
        return False

def update_user_name(mobile, name):
    '''
    @note: 修改昵称
    '''
    try:
        int(name)
        return False, u'昵称不能全是数字'
    except:
        pass
    if g.db.query(Customer).filter(Customer.name == name).first():
        return False, u'昵称已使用'
    user = g.db.query(Customer).filter(Customer.mobile == mobile).first()
    if user:
        user.name = name
        g.db.add(user)
        g.db.commit()
        return True, u'修改成功'
    else:
        return False, u'找不到用户'

def update_user_mobile(user_id, mobile):
    '''
    @note: 修改电话号码
    '''
    if len(mobile) != 11:
        return False, u'请输入11位手机号!'
    if g.db.query(Customer).filter(Customer.mobile == mobile).first():
        return False, u'手机已使用'
    user = g.db.query(Customer).filter(Customer.id == user_id).first()
    if user:
        user.mobile = mobile
        g.db.add(user)
        g.db.commit()
        return True, u'修改成功'
    return False, u'找不到用户'


def update_user_password(user_id, password):
    '''
    @note: 修改用户密码
    '''
    if len(password) < 4:
        return False, u'新密码不能少于4位!'
    user = g.db.query(Customer).filter(Customer.id == user_id).first()
    if user:
        user.password = password
        g.db.add(user)
        g.db.commit()
        return True, u'修改成功'
    return False, u'找不到用户'

def get_notification(user_id):
    '''
    @note: 获取通知数目
    '''
    return 0


