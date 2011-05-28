from django.db import models

import django.contrib.auth.models as auth


class Subscriber (auth.User):
    class Meta:
        # For now a Subscriber has no fields additional to a User, so it is just
        # a proxy.
        proxy = True
    
class Subscription (models.Model):
    METHOD_CHOICES = (
        ('email', 'Email'),
    )
    
    subscriber = models.ForeignKey('Subscriber')
    method = models.CharField(max_length=5, choices=METHOD_CHOICES, default="email")
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

