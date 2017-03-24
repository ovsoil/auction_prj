from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import View, TemplateView
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect
#  from weixin.client import WeixinAPI
from weixin.client import WeixinMpAPI
from weixin.oauth2 import OAuth2AuthExchangeError
from django.http import HttpResponse, HttpResponseServerError, Http404
import hashlib
import json
#  from lxml import etree
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


WEIXIN_TOKEN = 'testtoken'


class IndexView(TemplateView):
    template_name = 'index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


@csrf_exempt
def WechatMain(request):
    """
    """
    if request.method == "GET":
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("wechat  main")
    else:
        #  xml_str = smart_str(request.body)
        #  request_xml = etree.fromstring(xml_str)
        #  response_xml = request_xml
        return HttpResponse('Hello wechat')


class WechatApiView(View):
    #  appid, appsecret
    APP_ID = settings.APP_ID
    APP_SECRET = settings.APP_SECRET
    REDIRECT_URI = settings.REDIRECT_URI
    api = WeixinMpAPI(appid=APP_ID,
                      app_secret=APP_SECRET,
                      redirect_uri=REDIRECT_URI)


class WechatAuthView(WechatApiView):
    def get(self, request):
        path = request.GET.get('path')
        if path:
            #  if 'user' in request.session:
            #      return redirect(path)
            #  else:
            authorize_url = self.api.get_authorize_url(scope='snsapi_userinfo')
            print 'weixin authorize url: ', authorize_url
            return redirect(authorize_url)
        else:
            return Http404('parameter path not founded!')


class WechatRegisterView(WechatApiView):
    def get(self, request):
        code = request.GET.get('code')

        if code:
            # get access_token
            access_token = self.api.exchange_code_for_access_token(code=code)
            # get user info
            user_info = WeixinMpAPI(access_token=access_token).user(openid="openid")
            # save user info
            user = self._save_user(user_info)
            if not user:
                return HttpResponseServerError('save userinfo error')
            # store user info session
            #  request.session['user'] = user
            return redirect('/')

        else:
            # customer refuse authorize
            return Http404('parameter path or code not founded!!')

    def _save_user(self, data):
        user_data = {
            'nick': data['nickname'].encode('iso8859-1').decode('utf-8'),
            'openid': data['openid'],
            'avatar': data['headimgurl'],
            'info': self._user2utf8(data),
        }
        print user_data
        return user_data
        #  user = User.objects.filter(openid=data['openid'])
        #
        #  if 0 == user.count():
        #      user_data = {
        #          'nick': data['nickname'].encode('iso8859-1').decode('utf-8'),
        #          'openid': data['openid'],
        #          'avatar': data['headimgurl'],
        #          'info': self._user2utf8(data),
        #      }
        #      if 'unionid' in data:
        #          user_data.update('unionid', data.unionid)
        #      try:
        #          new_user = User(**user_data)
        #          new_user.save()
        #          user_data.update({'id': new_user.id})
        #          return user_data
        #      except Exception, e:
        #          log_err(e)
        #          return None
        #  else:
        #      return UserSerializer(user[0]).data

    def _user2utf8(self, user_dict):
        utf8_user_info = {
            "openid": user_dict['openid'],
            "nickname": user_dict['nickname'].encode('iso8859-1').decode('utf-8'),
            "sex": user_dict['sex'],
            "province": user_dict['province'].encode('iso8859-1').decode('utf-8'),
            "city": user_dict['city'].encode('iso8859-1').decode('utf-8'),
            "country": user_dict['country'].encode('iso8859-1').decode('utf-8'),
            "headimgurl": user_dict['headimgurl'],
            "privilege": user_dict['privilege'],
        }

        if 'unionid' in user_dict:
            utf8_user_info.update({'unionid': user_dict['unionid']})

        return utf8_user_info
