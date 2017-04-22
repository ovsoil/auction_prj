#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import simplejson
import urllib
import time
import random
import string
import hashlib
import logging


log = logging.getLogger('wechatapi')


class ApiError(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


class WechatBaseApi(object):

    API_PREFIX = u'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, appsecret, api_entry=None):
        self._appid = appid
        self._appsecret = appsecret
        self._access_token = None
        self.api_entry = api_entry or self.API_PREFIX

    @property
    def access_token(self):
        if not self._access_token:
            token, err = self.get_access_token()
            if not err:
                self._access_token = token['access_token']
                return self._access_token
            else:
                return None
        return self._access_token

    # parse json
    def _process_response(self, rsp):
        if 200 != rsp.status_code:
            return None, APIError(rsp.status_code, 'http error')
        try:
            content = rsp.json()
        except Exception:
            return None, APIError(9999, 'invalid response')
        if 'errcode' in content and content['errcode'] != 0:
            return None, APIError(content['errcode'], content['errmsg'])
        return content, None

    def _get(self, path, params=None):
        if not params:
            params = {}
        params['access_token'] = self.access_token
        rsp = requests(self.api_entry + path, params=params)

        return self._process_response(rsp)

    def _post(self, path, data, type='json'):
        header = {'content-type': 'application/json'}
        if '?' in path:
            url = self.api_entry + path + 'access_token=' + self.access_token
        else:
            url = self.api_entry + path + '?' + 'access_token=' + self.access_token
        if 'json' == type:
            data = simplejson.dumps(data, ensure_ascii=False).encode('utf-8')
        rsp = requests.post(url, data, headers=header)

        return self._process_response(rsp)


class WechatApi(WechatBaseApi):

    def get_access_token(self, url=None, **kwargs):
        params = {'grant_type': 'client_credential', 'appid': self._appid, 'secret': self._appsecret}
        if kwargs:
            params.update(kwargs)
        rsp = requests.get(url or self.api_entry + 'token', params)
        return self._process_response(rsp)

    # authorize url
    # https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
    def auth_url(self, redirect_uri, scope='snsapi_userinfo', state=None):
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' % \
              (self._appid, urllib.quote(redirect_uri), scope, state if state else '')
        return url

    # get authorize access_token
    def get_auth_access_token(self, code):
        url = u'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': self._appid,
            'secret': self._appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        return self._process_response(requests.get(url, params=params))

    # get user info
    def get_user_info(self, auth_access_token, openid):
        url = u'https://api.weixin.qq.com/sns/userinfo?'
        params = {
            'access_token': auth_access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        return self._process_response(requests.get(url, params=params))

    # get_jsapi_ticket
    def get_jsapi_ticket(self, auth_access_token):
        url = u'https://api.weixin.qq.com/cgi-bin/ticket/getticket?'
        params = {
            'access_token': auth_access_token,
            'type': 'jsapi'
        }
        return self._process_response(requests.get(url, params=params))


class Sign:
    def __init__(self, jsapi_ticket, url, debug=True):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }
        self._debug = debug

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def get_sign_data(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        return {
            'debug': self._debug,
            'appId': self._appid,
            'timestamp': self.ret['timestamp'],
            'nonceStr': self.ret['nonceStr'],
            'signature': hashlib.sha1(string).hexdigest()
        }