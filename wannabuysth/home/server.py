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

import requests
import urllib
class QQOAuth2Mixin(object):

    _OAUTH_CONSUMER_KEY = '100538015'
    _OAUTH_CONSUMER_SECRET = 'a7886775fc0564f27ef3b0fa642e6d93'

    _OAUTH_AUTHORIZE_URL = 'https://open.t.qq.com/cgi-bin/oauth2/authorize?'
    _OAUTH_ACCESS_TOKEN_URL = 'https://open.t.qq.com/cgi-bin/oauth2/access_token?'
    _OAUTH_API_URL = 'https://open.t.qq.com/api/%s'
    _OAUTH_VERSION = '2.a'
    redirect_uri = 'http://www.qp197.com:8000/home/oauth/qq'



    def get_authorize_redirect(self):
        url = "%sresponse_type=code&client_id=%s&scope=get_user_info,add_share&redirect_uri=%s" % (self._OAUTH_AUTHORIZE_URL, self._OAUTH_CONSUMER_KEY, self.redirect_uri)
        return url

    def get_authenticated_user(self, code):
        args = {
          "grant_type":'authorization_code',
          "code": code,
          "client_id": self._OAUTH_CONSUMER_KEY,
          "client_secret": self._OAUTH_CONSUMER_SECRET,
          "redirect_uri":self.redirect_uri
        }
        request_url = self._OAUTH_ACCESS_TOKEN_URL + urllib.urlencode(args)
        response = requests.get(request_url)
        content = response.content
        content = content.split('&')
        content = dict([[s.split('=')[0], s.split('=')[1]] for s in content if len(s.split('=')) == 2])
        return content



