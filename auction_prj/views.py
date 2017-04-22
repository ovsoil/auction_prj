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
