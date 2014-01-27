# -*- coding: UTF-8 -*-

from flask import g
from models import Customer
from models import Notification

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
    try:
        int(mobile)
    except:
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

def update_bind_mobile(user, mobile, password):
    '''
    @note: 绑定帐号
    '''
    if len(mobile) != 11:
        return False, u'请输入11位手机号!'
    try:
        int(mobile)
    except:
        return False, u'请输入11位手机号!'
    if g.db.query(Customer).filter(Customer.mobile == mobile).first():
        return False, u'手机已使用'
    user.mobile = mobile
    user.password = password
    g.db.add(user)
    g.db.commit()
    return True, u'绑定成功'


def update_user_password(user_id, password):
    '''
    @note: 修改用户密码
    '''
    if len(password) < 6:
        return False, u'新密码不能少于6位!'
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
    return g.db.query(Notification).filter(Notification.customer_id == user_id,
                                           Notification.is_visit == False
                                           ).count()

import requests
import urllib
import json
class QQOAuth2Mixin(object):

    _OAUTH_CONSUMER_KEY = '100538015'
    _OAUTH_CONSUMER_SECRET = 'a7886775fc0564f27ef3b0fa642e6d93'

    _OAUTH_CONSUMER_KEY = '100538712'
    _OAUTH_CONSUMER_SECRET = '82e30dd675f209c0ae500a3fdae02e4a'

    _OAUTH_AUTHORIZE_URL = 'https://graph.qq.com/oauth2.0/authorize?'
    _OAUTH_ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token?'
    _OAUTH_ACCESS_OPEN_ID_URL = 'https://graph.z.qq.com/moc2/me?'

    _OAUTH_USERINFO = 'https://graph.qq.com/user/get_simple_userinfo?'


    _OAUTH_VERSION = '2.a'
    redirect_uri = 'http://app.bangban.com/home/oauth/qq'


    def get_authorize_redirect(self, display="mobile"):
        url = "%sresponse_type=code&client_id=%s&scope=get_user_info,add_share&redirect_uri=%s&state=%s&display=%s" % \
        (self._OAUTH_AUTHORIZE_URL, self._OAUTH_CONSUMER_KEY, self.redirect_uri + '?display=%s' % display, 'bangban', display)
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
        if content.has_key('access_token'):
            access_token = content['access_token']
            args = {
                   'access_token':access_token
                   }
            request_url = self._OAUTH_ACCESS_OPEN_ID_URL + urllib.urlencode(args)
            response = requests.get(request_url)
            temp = response.content
            temp = temp.split('&')
            temp = dict([[s.split('=')[0], s.split('=')[1]] for s in temp if len(s.split('=')) == 2])
            content.update(temp)
        return content

    def get_user_info(self, access_token, openid):
        args = {
               'access_token':access_token,
               'oauth_consumer_key':self._OAUTH_CONSUMER_KEY,
               'openid':openid,
               'format':'json'
               }
        request_url = self._OAUTH_USERINFO + urllib.urlencode(args)
        response = requests.get(request_url)
        content = json.loads(response.content)
        return content






