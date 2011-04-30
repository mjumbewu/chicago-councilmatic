#will send out daily email for users - first will read all keywords
#create text files, then email text files to all each user subscribed.

from django.core.management.base import BaseCommand, CommandError
import smtplib, poplib
import django, datetime
from email.mime.text import MIMEText
from phillyleg.models import Subscription, KeywordSubscription, LegFile
from django.utils.encoding import smart_str, smart_unicode

class Command(BaseCommand):
	help = "This script sends daily digests out to subscribers."
	EMAIL_TITLE = "PHILLY COUNCILMATIC " + datetime.date.today().__str__()
	DIVIDER = "====================================\n"
	SINGLE_DIVIDER = "-----------------------------------------------------------------"
	
	def send_email(self, you, emailbody):
		smtphost = "smtp.gmail.com"
		smtpport = '465'
		me =  'philly.legislative.list'
		msg = MIMEText(smart_str(emailbody))
		msg['Subject'] = self.EMAIL_TITLE
		msg['From'] = me
		msg['To'] = you
		s = smtplib.SMTP_SSL(smtphost, smtpport)
		s.login(me, 'phillydatacamp')
		s.sendmail(me, [you], msg.as_string())
		s.quit()

	def handle(self, *args, **options):
		emails = Subscription.objects.all()
		emailbody = self.EMAIL_TITLE+"\n"
		today = datetime.date.today()
		
		for em in emails:
			legfile_set = set()
			
			# Collect all the keyword subscriptions.
			for k in em.keywords.all():
				if not k.keyword:
					continue
				
				legfiles = LegFile.objects\
					.filter(title__icontains=k)\
					.filter(last_scraped__range=(em.last_sent,today))
					
				# Add files to a set to remove duplicates, if any exist.  There
				# may be duplicates if, for example, a user subscribes to two 
				# keywords and both match some of the same bills.
				for legfile in legfiles:
					legfile_set.add(legfile)
			
			# Collect all the councilmember subscriptions.
			for cm in em.councilmembers.all():
				
				legfiles = LegFile.objects\
					.filter(last_scraped__range=(em.last_sent,today))
				
				# Add files to the same set as above.
				for legfile in legfiles:
				    if cm in legfile.sponsors.all():
    					legfile_set.add(legfile)
					
			# Write emails for all the selected leg files
			emailbody = self.makeBillEmail(
				legfile_set, 
				keywords=[str(k) for k in em.keywords.all()],
				councilmembers=[str(cm) for cm in em.councilmembers.all()])
			
			# Send the email
			self.send_email(unicode(em), emailbody)
			em.last_sent = datetime.date.today()
			em.save()
			
	def makeBillEmail(self, bills, keywords=None, councilmembers=None):
		body = self.DIVIDER
		if keywords:
			body += "Keywords: %s\n" %  (','.join(keywords))
		if councilmembers:
		    body += "Councilmembers: %s\n" % (','.join(councilmembers))
		body += self.DIVIDER +"\n"
		
		for bill in bills:
			bill_body = bill.title + "\n\n"
			bill_body += "Sponsors: %s\n\n" % \
				(', '.join([s.name for s in bill.sponsors.all()]))
			bill_body += "Current Status: %s\n\n" % bill.status
			bill_body += "Full Text and more information: %s\n\n" % bill.url
			body += "\n%s\n%s\n" % (bill_body, self.SINGLE_DIVIDER)
		
		return body
		
	
	
