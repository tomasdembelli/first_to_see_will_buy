from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_init, pre_save
from django.dispatch import receiver

# Create your models here.
'''
class User(models.Model):
    user_name = models.CharField(max_length=20)
    default = 1

    def __str__(self):
        return self.user_name
'''

class Ad(models.Model):
    title = models.CharField('Title ', max_length=100)
    #ad_category : will be selectable through options 
    #ad_negotiation_history : will show the messages in reverse chronological order
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField('Description ', max_length=500)
    #ad_zip : will use regex
    price = models.IntegerField('Price ',default=1)
    #pub_date = models.DateField('date published', default=timezone.now)    # force to choose today and future
    pub_date = models.DateTimeField('date published', auto_now_add=True)    #auto_now_add : saves the first creation time. auto_now is updated at every update.    # force to choose today and future
    
    def publish(self):
        old = 1000    #Ads older than 'old' won't be shown
        now = timezone.now()
        return now - datetime.timedelta(days=old) <= self.pub_date <= now

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)    # when querying all ads, they will be ordered by pu_date in reverse order
    

class Message(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    sent_time = models.DateTimeField(auto_now_add=True, )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
    class Meta:
        get_latest_by = 'sent_time'
    '''

    def __str__(self):
        return self.text


class FavouriteAd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.ad.title



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

