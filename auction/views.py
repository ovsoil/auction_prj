from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import views, viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from auction.models import Good, Bid
from authentication.models import Account
from auction.serializers import GoodSerializer, BidSerializer
from authentication.permissions import IsSupperUser, IsAuthenticated
#  from auction.authenticators import QuietBasicAuthentication
from django.contrib.auth.models import AnonymousUser
import json


class GoodViewSet(viewsets.ModelViewSet):
    """
    endipoint presents auction goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (IsSupperUser(),)

    @detail_route
    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def details(self, request, *args, **kwargs):
        good = self.get_object()
        return Response(good.details)


class BidViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if self.request.method == 'POST':
            return (IsAuthenticated(),)
        return (IsSupperUser(),)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(bidder=self.request.user, good=Good.objects.get(id=self.request.data['good_id']))
        else:
            if self.request.session.get('user'):
                user = Account.objects.get(username=self.request.session['user']['username'])
                serializer.save(bidder=user, good=Good.objects.get(id=self.request.data['good_id']))
        return super(BidViewSet, self).perform_create(serializer)


class GoodBidViewSet(viewsets.ViewSet):
    """
    """
    queryset = Bid.objects.select_related('good')       # .order_by('-time')
    serializer_class = BidSerializer

    def list(self, request, good_pk=None):
        bids = self.queryset.filter(good=good_pk)
        serializer = self.serializer_class(bids, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, good_pk=None):
        bids = self.queryset.get(pk=pk, good=good_pk)
        serializer = self.serializer_class(bids, many=False, context={'request': request})
        return Response(serializer.data)


class AccountBidViewSet(viewsets.ViewSet):
    queryset = Bid.objects.select_related('bidder')       # .order_by('-time')
    serializer_class = BidSerializer

    def list(self, request, account_pk=None):
        bids = self.queryset.filter(bidder=account_pk)
        serializer = self.serializer_class(bids, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, bidder_pk=None):
        bids = self.queryset.get(pk=pk, bidder=bidder_pk)
        serializer = self.serializer_class(bids, many=False, context={'request': request})
        return Response(serializer.data)
