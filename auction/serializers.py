from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from auction.models import Good, Bid, Image
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class GoodSerializer(serializers.HyperlinkedModelSerializer):
    # details = serializers.HyperlinkedIdentityField(view_name='good-details', format='html')
    # images = serializers.ListField(child=serializers.ImageField(allow_empty_file=True))
    images = serializers.SerializerMethodField()

    class Meta:
        model = Good
        fields = ('url', 'id', 'name', 'description', 'slogan', 'images', 'start_time', 'stop_time',
                  'start_price', 'bid_range', 'status', 'post_time', 'details', 'visitor_num')
        read_only_fields = ('post_time',)

    def get_images(self, obj):
        files = [getattr(obj, 'image%02d' % i).name for i in range(1, 10)]
        return [staticfiles_storage.url(f) for f in files if f]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # bids = serializers.HyperlinkedRelatedField(queryset=Bid.objects.all(), view_name='bid-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.username)
        password = validated_data.get('password', None)
        instance.set_password(password)
        instance.save()
        update_session_auth_hash(self.context.get('request'), instance)
        return instance


class BidSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    #  user = serializers.HyperlinkedRelatedField(
    #      view_name='user-detail',
    #      #  lookup_field='username',
    #      lookup_field='pk',
    #      many=False,
    #      read_only=True
    #  )
    good = serializers.ReadOnlyField(source='good.name')
    #  good = serializers.HyperlinkedRelatedField(
    #      view_name='good-detail',
    #      #  lookup_field='id',
    #      lookup_field='pk',
    #      many=False,
    #      read_only=True
    #  )

    class Meta:
        model = Bid
        fields = ('url', 'id', 'time', 'price', 'user', 'good')

    def create(self, validated_data):
        return Bid.objects.create(**validated_data)


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('url', 'id', 'name', 'img')
