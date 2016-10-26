from rest_framework import serializers
from auction.models import Good, Bid
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class GoodSerializer(serializers.HyperlinkedModelSerializer):
    # details = serializers.HyperlinkedIdentityField(view_name='good-details', format='html')
    # images = serializers.ListField(child=serializers.ImageField(allow_empty_file=True))
    image01 = serializers.SerializerMethodField()
    image02 = serializers.SerializerMethodField()
    image03 = serializers.SerializerMethodField()
    image04 = serializers.SerializerMethodField()

    class Meta:
        model = Good
        fields = ('url', 'id', 'name', 'description', 'image01', 'image02', 'image03', 'image04', 'start_time', 'stop_time',
                  'start_price', 'bid_range', 'bidder_num', 'status', 'post_time', 'details')
        read_only_fields = ('post_time',)

    def get_image01(self, obj):
        return staticfiles_storage.url(obj.image01.name)

    def get_image02(self, obj):
        return staticfiles_storage.url(obj.image02.name)

    def get_image03(self, obj):
        return staticfiles_storage.url(obj.image03.name)

    def get_image04(self, obj):
        return staticfiles_storage.url(obj.image04.name)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    bids = serializers.HyperlinkedRelatedField(queryset=Bid.objects.all(), view_name='bid-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'bids')


class BidSerializer(serializers.HyperlinkedModelSerializer):
    bidder = serializers.ReadOnlyField(source='bidder.username')
    bidfor = serializers.ReadOnlyField(source='bidfor.name')

    class Meta:
        model = Bid
        fields = ('url', 'id', 'time', 'amount', 'bidder', 'bidfor')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(BidSerializer, self).get_validation_exclusions()
        return exclusions + ['bidder', 'bidfor']
