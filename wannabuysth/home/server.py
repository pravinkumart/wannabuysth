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



def get_notification(user_id):
    '''
    @note: 获取通知数目
    '''
    return 0


