from __future__ import unicode_literals
from authentication.models import Account
from django.db import models
from datetime import datetime
from redactor.fields import RedactorField


class Image(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/', blank=True, null=True)
    post_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-post_time', )

    def __unicode__(self):
        return self.name


# Create your models here.
class Good(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    slogan = models.TextField(default='')
    banner_image = models.ImageField(upload_to='images/')

    image01 = models.ImageField(upload_to='images/')
    image02 = models.ImageField(upload_to='images/', blank=True, null=True)
    image03 = models.ImageField(upload_to='images/', blank=True, null=True)
    image04 = models.ImageField(upload_to='images/', blank=True, null=True)
    image05 = models.ImageField(upload_to='images/', blank=True, null=True)
    image06 = models.ImageField(upload_to='images/', blank=True, null=True)
    image07 = models.ImageField(upload_to='images/', blank=True, null=True)
    image08 = models.ImageField(upload_to='images/', blank=True, null=True)
    image09 = models.ImageField(upload_to='images/', blank=True, null=True)

    post_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)
    start_price = models.IntegerField()
    bid_range = models.IntegerField()
    details = RedactorField(verbose_name=u'Text')
    visitor_num = models.IntegerField(default=0)

    # bidder_num = models.IntegerField(default=0)
    # praise_num = models.IntegerField(default=0)
    # comment_num = models.IntegerField(default=0)

    @property
    def status(self):
        tz_info = self.start_time.tzinfo
        if self.stop_time < datetime.now(tz_info):
            return 'done'
        elif self.start_time > datetime.now(tz_info):
            return 'comming'
        else:
            return 'going'

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('-start_time', '-stop_time')


class Bid(models.Model):
    bidder = models.ForeignKey(Account, on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField()

    class Meta:
        ordering = ('-time', )

    def __unicode__(self):
        return '{0}: {1}'.format(self.bidder, self.price)
