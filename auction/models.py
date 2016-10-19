from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    image = models.CharField(max_length=100, blank=True, default='')
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)
    start_price = models.IntegerField()
    bid_range = models.IntegerField()
    bidder_num = models.IntegerField(default=0)
    # current_bid = models.ForeignKey('auction.Bid', related_name='item')
    post_time = models.DateTimeField(auto_now_add=True)

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
        ordering = ('post_time',)



class Bid(models.Model):
    bidder = models.ForeignKey(User)
    # bidder = models.ForeignKey('User', related_name='bid')
    bid_item = models.ForeignKey(Item)
    # bid_item = models.ForeignKey('auction.Item', related_name='bid')
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    class Meta:
        ordering = ('time', )

    def __unicode__(self):
        return '{0}: {1}'.format(self.bidder, self.amount)
