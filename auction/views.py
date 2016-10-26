from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from auction.models import Good, Bid
from auction.serializers import UserSerializer, GoodSerializer, BidSerializer


# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GoodViewSet(viewsets.ModelViewSet):
    """
    endipoint presents auction goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(), IsBidderOfBid(),)

    def perform_create(self, serializer):
        instance = serializer.save(bidder=self.request.user,
                                   bidfor=self.request.good)

        return super(BidViewSet, self).perform_create(serializer)


class UserBidViewSet(viewsets.ViewSet):
    queryset = Bid.objects.select_related('bidder').order_by('-time')
    serializer_class = BidSerializer

    def list(self, request, user_username=None):
        queryset = self.queryset.filter(author__username=user_username)
        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)
