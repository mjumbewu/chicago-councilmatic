#will send out daily email for users - first will read all keywords
#create text files, then email text files to all each user subscribed.

from email.mime.text import MIMEText
from itertools import chain
import datetime
import poplib
import smtplib

import django
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import smart_str, smart_unicode

from subscriptions.management.feeds import FeedCollector
from subscriptions.models import Subscriber

class Command(BaseCommand):
    help = "This script sends daily digests out to subscribers."
    EMAIL_TITLE = "PHILLY COUNCILMATIC " + datetime.date.today().__str__()
    DIVIDER = "====================================\n"
    SINGLE_DIVIDER = "-----------------------------------------------------------------"
    
    def send_email(self, you, emailbody, emailsubject=None):
        smtphost = "smtp.gmail.com"
        smtpport = '465'
        me =  'philly.legislative.list'
        msg = MIMEText(smart_str(emailbody))
        msg['Subject'] = emailsubject or self.EMAIL_TITLE
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP_SSL(smtphost, smtpport)
        s.login(me, 'phillydatacamp')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
    
    def get_new_content_in(self, subscription):
        feed = subscription.feed
        last_sent = subscription.last_sent
        
        collector = FeedCollector()
        new_content = collector.collect_new_content(feed, last_sent)
        return new_content
    
    def get_new_content_for(self, subscriber):
        new_content = chain(self.get_new_content_in(subscription)
                            for subscription in subscriber.subscriptions.all())
        return set(list(new_content)[0])
        
    def handle(self, *args, **options):
        new_content = {}
        
        # We're ignoring channels for now.
        subscribers = Subscriber.objects.all()
        for subscriber in subscribers:
            new_content = self.get_new_content_for(subscriber)
        
            emailbody = self.EMAIL_TITLE+"\n"
            now = datetime.datetime.now()
            
            # TODO: The SubscriptionDispatcher should do all of the following
            
            # Write emails for all the selected content
            emailbody = self.make_feed_email(
                new_content, 
                subscriber.subscriptions)
            
            # Send the email
            self.send_email(subscriber.email, emailbody)
            
            # Update the subscription last sent time
            for subscription in subscriber.subscriptions.all():
                subscription.last_sent = now
                subscription.save()
            
    def make_feed_email(self, content, subscriptions):
        body = self.DIVIDER
        body += "Subscriptions: %s\n" % subscriptions
        body += self.DIVIDER + "\n"
        
        for item in content:
            body += "\n%s\n\n" % item
            body += "More at %s\n\n" % item.get_absolute_url()
            body += self.DIVIDER + "\n"
        
        return body
        
    
    
