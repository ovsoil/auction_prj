from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        print username
        if not username:
            raise ValueError('Users must have a valid username.')
        account = self.model(username=username, **extra_fields)
        account.is_superuser = False
        account.is_staff = False
        if not username.startswith('wx_'):
            account.set_password(password)
        account.save()
        return account

    def create_superuser(self, username, password, **kwargs):
        account = self.create_user(username, password, **kwargs)
        account.is_superuser = True
        account.is_staff = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(blank=True)

    # for wechat user
    openid = models.CharField(max_length=40)
    nickname = models.CharField(max_length=40)
    avatar = models.ImageField(upload_to='images/', blank=True, null=True)
    #  info = models.CharField(max_length=140, blank=True)

    phone = models.CharField(max_length=20)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'
    # for createsupoeruser
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.username, self.email])

    def get_short_name(self):
        return self.username
