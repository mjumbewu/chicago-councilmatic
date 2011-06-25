from django.db import models

import django.contrib.auth.models as auth


class DistributionChannel (models.Model):
    recipient = models.ForeignKey(auth.User, null=True)

class EmailChannel (DistributionChannel):
    email = models.CharField(max_length=256)

class RssChannel (DistributionChannel):
    pass

class SmsChannel (DistributionChannel):
    number = models.CharField(max_length=32)
    carrier = models.CharField(max_length=32)

    
class Subscription (models.Model):
    channel = models.ForeignKey('DistributionChannel', null=True)
    last_sent = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        
        # We could use Django's built-in ability to make this an auto_now field,
        # but then we couldn't change the value when we want.
        if not self.id:
            self.last_sent = datetime.datetime.now()
        super(Subscription, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.email

class SearchSubscription (Subscription):
    query = models.TextField()
    
    def __unicode__(self):
        return self.query

