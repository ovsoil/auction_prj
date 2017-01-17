from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from redactor.fields import RedactorField


# Create your models here.
class Good(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    image01 = models.ImageField(upload_to='images/', blank=True, null=True, default='01.jpg')
    image02 = models.ImageField(upload_to='images/', blank=True, null=True, default='02.jpg')
    image03 = models.ImageField(upload_to='images/', blank=True, null=True, default='03.jpg')
    image04 = models.ImageField(upload_to='images/', blank=True, null=True, default='04.jpg')
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)
    start_price = models.IntegerField()
    bid_range = models.IntegerField()
    bidder_num = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)
    details = RedactorField(verbose_name=u'Text')

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
        ordering = ('start_time',)


class Bid(models.Model):
    #  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #  good = models.ForeignKey('auction.Good', on_delete=models.CASCADE, related_name='bids')
    #  good = models.ForeignKey('auction.Good', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

    class Meta:
        ordering = ('time', )

    def __unicode__(self):
        return '{0}: {1}'.format(self.user, self.amount)
