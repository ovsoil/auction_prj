from rest_framework import serializers
from auction.models import Good, Bid
from django.contrib.auth.models import User


class GoodSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Good
        fields = ('url', 'id', 'name', 'description', 'image', 'start_time', 'stop_time',
                  'start_price', 'bid_range', 'bidder_num', 'status', 'post_time')
        read_only_fields = ('post_time',)


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
