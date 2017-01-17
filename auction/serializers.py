from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from auction.models import Good, Bid
from django.contrib.auth.models import User
from django.contrib.staticfiles.storage import staticfiles_storage


class GoodSerializer(serializers.HyperlinkedModelSerializer):
    # details = serializers.HyperlinkedIdentityField(view_name='good-details', format='html')
    # images = serializers.ListField(child=serializers.ImageField(allow_empty_file=True))
    images = serializers.SerializerMethodField()

    class Meta:
        model = Good
        fields = ('url', 'id', 'name', 'description', 'images', 'start_time', 'stop_time',
                  'start_price', 'bid_range', 'bidder_num', 'status', 'post_time', 'details')
        read_only_fields = ('post_time',)

    def get_images(self, obj):
        return [
            staticfiles_storage.url(obj.image01.name),
            staticfiles_storage.url(obj.image02.name),
            staticfiles_storage.url(obj.image03.name),
            staticfiles_storage.url(obj.image04.name),
        ]


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'id', 'username', 'password', 'first_name',
#                   'last_name', 'email')
#         read_only_fields = ('id',)
#         write_only_fields = ('password',)

#     def restore_object(self, attrs, instance=None):
#         user = super(UserSerializer, self).restore_object(attrs, instance)
#         user.set_password(attrs['password'])
#         return user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    # bids = serializers.HyperlinkedRelatedField(queryset=Bid.objects.all(), view_name='bid-detail', many=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # user = User.objects.create(
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
        fields = ('url', 'id', 'time', 'amount', 'user', 'good')

    def create(self, validated_data):
        return Bid.objects.create(**validated_data)

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(BidSerializer, self).get_validation_exclusions()
        return exclusions + ['user', 'good']
