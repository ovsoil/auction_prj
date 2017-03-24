from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('url', 'id', 'username', 'email',
                  'openid', 'nickname', 'avatar', 'phone',
                  'created_at', 'updated_at', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.save()
            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)
            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()
            update_session_auth_hash(self.context.get('request'), instance)
            return instance
