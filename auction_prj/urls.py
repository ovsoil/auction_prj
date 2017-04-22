"""auction_prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from auction.views import GoodViewSet, BidViewSet
from auction.views import GoodBidViewSet, AccountBidViewSet
from authentication.views import AccountViewSet
from authentication.views import AuthView, WechatAuthView, WechatRegisterView
from auction_prj.views import IndexView, WechatMain
#  from django.contrib.staticfiles import views
from django.conf import settings
from django.conf.urls.static import static


router = routers.SimpleRouter()
router.register(r'goods', GoodViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'bids', BidViewSet)

accounts_router = routers.NestedSimpleRouter(
    router, r'accounts', lookup='account'
)
accounts_router.register(r'bids', AccountBidViewSet, base_name='account-bids')

goods_router = routers.NestedSimpleRouter(
    router, r'goods', lookup='good'
)
goods_router.register(r'bids', GoodBidViewSet, base_name='good-bids')

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(accounts_router.urls)),
    url(r'^api/v1/', include(goods_router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/auth/$', AuthView.as_view(), name='authenticate'),
    url(r'^api/v1/auth/wechat/$', WechatAuthView.as_view(), name='wechat_auth'),
    url(r'^api/v1/login/wechat/$', WechatRegisterView.as_view(), name='wechat_login'),
    url(r'^wechat-main/$', WechatMain, name='wechat_main'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^.*$', IndexView.as_view(), name='index'),
]
