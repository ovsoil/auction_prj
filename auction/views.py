from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import views, viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from auction.models import Good, Bid
from auction.serializers import UserSerializer, GoodSerializer, BidSerializer
from auction.permissions import IsSupperUser, IsStaffOrTargetUser
#  from auction.authenticators import QuietBasicAuthentication
import json
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (permissions.AllowAny,)

        return super(UserViewSet, self).get_permissions()


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
            return (permissions.IsAuthenticated(),)
        return (IsSupperUser(),)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        good=Good.objects.get(id=self.request.data['good_id']))

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
        serializer = self.serializer_class(bids, many=True, context={'request': request})
        return Response(serializer.data)


class UserBidViewSet(viewsets.ViewSet):
    queryset = Bid.objects.select_related('user')       #.order_by('-time')
    serializer_class = BidSerializer

    def list(self, request, user_pk=None):
        bids = self.queryset.filter(user=user_pk)
        serializer = self.serializer_class(bids, many=True, context={'request': request})
        return Response(serializer.data)


class AuthView(views.APIView):
    #  authentication_classes = (QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        if username is None:
            username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(instance=user, context={'request': request})
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'The password is valid, but the user has been disabled!'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response()
