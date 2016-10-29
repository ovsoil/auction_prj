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
from auction.views import UserViewSet, GoodViewSet, BidViewSet, UserBidViewSet, LoginView, LogoutView
from auction_prj.views import IndexView, AngularView

# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'goods', GoodViewSet)
# router.register(r'bids', BidViewSet)

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'goods', GoodViewSet)
router.register(r'bids', BidViewSet)

users_router = routers.NestedSimpleRouter(
    router, r'users', lookup='user'
)
users_router.register(r'bids', UserBidViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(users_router.urls)),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^(?P<template_name>[-_\w]+/$)', AngularView.as_view(), name='angular'),
    # url(r'^(?P<folder>[-_\w]+)/(?P<template_name>[-_\w]+/$)', AngularView.as_view(), name='angular_folder'),
    url(r'^.*$', IndexView.as_view(), name='index'),
]
