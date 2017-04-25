import os
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from auction.models import Good, Bid, Image
from django.contrib.staticfiles.storage import staticfiles_storage
from authentication.models import Account
from authentication.serializers import AccountSerializer


class GoodSerializer(serializers.HyperlinkedModelSerializer):
    # details = serializers.HyperlinkedIdentityField(view_name='good-details', format='html')
    # images = serializers.ListField(child=serializers.ImageField(allow_empty_file=True))
    images = serializers.SerializerMethodField()

    class Meta:
        model = Good
        fields = ('url', 'id', 'name', 'description', 'slogan', 'banner_image', 'images', 'start_time', 'stop_time',
                  'start_price', 'bid_range', 'status', 'post_time', 'details', 'visitor_num')
        read_only_fields = ('post_time',)

    def get_images(self, obj):
        files = [getattr(obj, 'image%02d' % i).name for i in range(1, 10)]
        return [os.path.join(settings.MEDIA_URL, f) for f in files if f]


class AccountField(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'nickname': value.nickname,
            'avatar': value.avatar_url
        }


class BidSerializer(serializers.HyperlinkedModelSerializer):
    #  bidder = serializers.HyperlinkedRelatedField(
    #      view_name='account-detail',
    #      lookup_field='pk',
    #      many=False,
    #      read_only=True
    #  )
    #  bidder = serializers.ReadOnlyField(source='bidder.nickname')
    #  bidder = AccountSerializer(many=False, read_only=True)
    bidder = AccountField(many=False, read_only=True)

    good = serializers.HyperlinkedRelatedField(
        view_name='good-detail',
        lookup_field='pk',
        many=False,
        read_only=True
    )

    class Meta:
        model = Bid
        fields = ('url', 'id', 'time', 'price', 'bidder', 'good')

    def create(self, validated_data):
        return Bid.objects.create(**validated_data)


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('url', 'id', 'name', 'img')
