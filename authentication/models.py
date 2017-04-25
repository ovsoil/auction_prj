from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a valid username.')
        account = self.model(username=username, **extra_fields)
        account.is_superuser = False
        account.is_staff = False
        if not account.nickname:
            account.nickname = username
        if not username.startswith('wx_'):
            account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, password, **kwargs):
        account = self.create_user(username, password, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        if not account.nickname:
            account.nickname = username
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(blank=True)

    # for wechat user
    openid = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64)
    avatar = models.ImageField(upload_to='images/', max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    # for createsupoeruser
    REQUIRED_FIELDS = ['email']

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return '/static/images/avatar.png'

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.username, self.email])

    def get_short_name(self):
        return self.username
