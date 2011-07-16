import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

#
# Legislative File models
#

class CouncilMember(models.Model):
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.name.lstrip("Councilmember")


class LegFile(models.Model):
    key = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=1000)
    controlling_body = models.CharField(max_length=1000)
    date_scraped = models.DateTimeField(auto_now_add=True)
    last_scraped = models.DateTimeField(auto_now=True)
    final_date = models.DateField(null=True)
    intro_date = models.DateField(null=True)
    sponsors = models.ManyToManyField(CouncilMember)
    status = models.CharField(max_length=1000)
    title = models.TextField()
    type = models.CharField(max_length=1000)
    url = models.CharField(max_length=2048)
    version = models.CharField(max_length=100)
    
    def __unicode__(self):
        return "(%s) %s%s" % (self.key, self.title[:100], 
            '...' if len(self.title) > 100 else '')
    
    @models.permalink
    def get_absolute_url(self):
        return ('legislation_detail', [str(self.pk)])

class LegFileAttachment(models.Model):
    file = models.ForeignKey(LegFile)
    description = models.CharField(max_length=1000)
    url = models.CharField(max_length=2048)
    fulltext = models.TextField()
    
    class Meta:
        unique_together = (('file','url'),)

class LegAction(models.Model):
    file = models.ForeignKey(LegFile)
    date_taken = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    minutes = models.ForeignKey('LegMinutes', null=True)
    motion = models.CharField(max_length=1000)
    acting_body = models.CharField(max_length=1000)
    notes = models.TextField()
    
    class Meta:
        unique_together = (('file','date_taken','description','notes'),)

class LegMinutes(models.Model):
    url = models.CharField(max_length=2048, primary_key=True)
    fulltext = models.TextField()
    date_taken = models.DateField(null=True)

    def __unicode__(self):
        return "(%s) %s%s" % (self.date_taken, self.fulltext[:100], 
            '...' if len(self.fulltext) > 100 else '')

#
# Subscription models
#

class Subscription(models.Model):
    email  = models.CharField(max_length=100)
    last_sent = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.last_sent = datetime.datetime.now()
        super(Subscription, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.email

class KeywordSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, related_name='keywords')
    keyword = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.keyword

class CouncilMemberSubscription(models.Model):
    subscription = models.ForeignKey(Subscription, related_name='councilmembers')
    councilmember = models.ForeignKey(CouncilMember)
    
    def __unicode__(self):
        return unicode(self.councilmember)


