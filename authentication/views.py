#  from django.shortcuts import render
from rest_framework import permissions
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from auction.models import Bid
from auction.serializers import BidSerializer
from authentication.models import Account
from authentication.permissions import IsAuthenticated, IsAccountOwner
from authentication.serializers import AccountSerializer
from django.views.generic import View
from auction_prj import settings
from authentication.wechat_api import WechatApi, ApiError, Sign
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import logging


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        # everyone can register new counter
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)
            return Response(serializer.validated_data,
                            status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class AuthView(views.APIView):
    #  authentication_classes = (QuietBasicAuthentication,)

    # /login : authenticate normal account
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        if username is None:
            username = Account.objects.get(email=email).username
        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)
                serialized = AccountSerializer(instance=account, context={'request': request})
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'The password is valid, but the account has been disabled!'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    # /logout
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()


class WechatApiView(View):
    APP_ID = settings.APP_ID
    APP_SECRET = settings.APP_SECRET
    HOST = settings.HOST
    REDIRECT_URI = settings.REDIRECT_URI
    api = WechatApi(appid=APP_ID, appsecret=APP_SECRET)


class WechatAuthView(WechatApiView):
    def get(self, request):
        path = request.GET.get('path')
        path = path if path else '/'
        if 'user' in request.session:
            logging.warning("user: %s in session" % request.session['user']['username'])
            return redirect(path)
        else:
            # TODO get redirect_uri from view&url
            logging.warning("wechat auth")
            redirect_uri = 'https://%s%s?path=%s' % (self.HOST, reverse('wechat_login'), path)
            authorize_url = self.api.auth_url(redirect_uri=redirect_uri,
                                              scope='snsapi_userinfo')
            return redirect(authorize_url)


class WechatRegisterView(WechatApiView):
    def get(self, request):
        code = request.GET.get('code')
        target_url = request.GET.get('path')

        if code:
            # get access_token
            token_data, error = self.api.get_auth_access_token(code)
            if error:
                return HttpResponseServerError('get access_token error')

            # get user info
            user_info, error = self.api.get_user_info(token_data['access_token'], token_data['openid'])
            if error:
                return HttpResponseServerError('get userinfo error')

            user = self._save_user(user_info, request)
            if not user:
                return HttpResponseServerError('save userinfo error')

            # save in session
            request.session['user'] = user

            # redirect to target url
            if target_url:
                return redirect(target_url)
            else:
                return redirect('/')
        else:
            # customer refuse authorize
            return HttpResponseNotFound('Parameter path or code not founded!')

    def _save_user(self, info, request):
        user = Account.objects.filter(openid=info['openid'])
        if 0 == user.count():
            user_data = {
                'openid': info['openid'],
                'nickname': info['nickname'].encode('iso8859-1').decode('utf-8'),
                'avatar': info['headimgurl'],
            }
            if 'unionid' in info:
                user_data.update('unionid', info.unionid)
            try:
                username = 'wx_' + user_data['nickname']
                new_account = Account(username=username, **user_data)
                new_account.save()
                user_data.update({'id': new_account.id})
            except Exception as e:
                return None
            return user_data
        else:
            return AccountSerializer(user[0], context={'request': request}).data

    def _user2utf8(self, user_dict):
        '''
        collect user info:
        {
            "openid":" OPENID",
            "nickname": NICKNAME,
            "sex":"1",
            "province":"PROVINCE"
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl":    "http://wx.qlogo.cn/mmopen/",
            "privilege":[ "PRIVILEGE1" "PRIVILEGE2"     ],
            "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        }
        '''
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


class WechatSdkView(WechatApiView):
    def post(self, request):
        url = request.GET.get('url')
        jsapi_ticket = self.api.get_jsapi_ticket()
        return Sign(jsapi_ticket, url).get_sign_data()
