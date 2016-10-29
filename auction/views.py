import json
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
from auction.permissions import IsSupperUser


# Create your views here.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(),)


class GoodViewSet(viewsets.ModelViewSet):
    """
    endipoint presents auction goods
    """
    queryset = Good.objects.all()
    serializer_class = GoodSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (IsSupperUser,)

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

        return (permissions.IsSupperUser,)

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


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = json.loads(request.body)
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                serialized = UserSerializer(user)
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This user has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
