import datetime
import ebdata.nlp.addresses
import re
import utils
from django.contrib.gis.db import models
from django.contrib.gis import geos
#from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#
# Metadata about the scraping process
#

class LegKeys(models.Model):
    continuation_key = models.IntegerField()


#
# Legislative File models
#

class CouncilMember(models.Model):
    name = models.CharField(max_length=100)
    headshot = models.CharField(max_length=255,
        # Path to councilmember image, relative to static files dir
        default='phillyleg/noun_project_416.png')

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
    sponsors = models.ManyToManyField(CouncilMember, related_name='legislation')
    status = models.CharField(max_length=1000)
    title = models.TextField()
    type = models.CharField(max_length=1000)
    url = models.URLField()
    version = models.CharField(max_length=100)

    class Meta:
        ordering = ['-key']

    def __unicode__(self):
        return "%s %s: %s%s" % (self.type, self.id, self.title[:100],
            '...' if len(self.title) > 100 else '')

    @models.permalink
    def get_absolute_url(self):
        return ('legislation_detail', [str(self.pk)])

    @property
    def last_action_date(self):
        """
        Gets the date of the latest action

        """
        actions = self.actions.all()

        if len(actions) == 0:
            return None

        return max([action.date_taken for action in actions])

    @property
    def timeline(self):
        """
        Gets a timeline object that represents the legfile actions grouped by
        ``date_taken``.

        """
        from collections import defaultdict
        class LegActionTimeline (defaultdict):
            def __init__(self):
                super(LegActionTimeline, self).__init__(list)

            def __iter__(self):
                return iter(sorted(self.keys()))

        timeline = LegActionTimeline()
        for action in self.actions.all():
            print action.date_taken
            timeline[action.date_taken].append(action)

        return timeline

    def all_text(self):
        if not hasattr(self, '_all_text'):
            att_text = [att.fulltext for att in self.attachments.all()]
            self._all_text = ' '.join([self.title] + att_text)
        return self._all_text

    def unique_words(self):
        """
        Gets all the white-space separated words in the file.  A word is
        anything that starts and ends with word characters and has no internal
        white space.

        """
        # Get rid of any punctuation on the outside of words.
        only_words = re.sub(r'(\s\W+|\W+\s|\W+$)', ' ', self.title)

        # Pick out and return the unique values by spliting on whitespace, and
        # lowercasing everything.
        unique_words = set(word.lower() for word in only_words.split())
        return unique_words

    def addresses(self):
        addresses = ebdata.nlp.addresses.parse_addresses(self.all_text())
        return addresses

    def mentioned_legfiles(self):
        """
        Gets a generator for any files (specifically, bills) mentioned in the
        file.

        """
        # Find all the strings that match the characteristic regular expression
        # for a bill id.
        id_matches = re.findall(r'\s(\d{6}(-A+)?)', self.title)

        # The id matches may each have two groups (the second of which will
        # contain only the A's).  We only care about the first.
        mentioned_legfile_ids = set(groups[0] for groups in id_matches)

        for mentioned_legfile_id in mentioned_legfile_ids:
            # It's possible that no legfile in our database may match the id
            # we've parsed out.  When this is the case, there's nothing we can
            # do about it, so just fail "silently" (with a log message).
            try:
                mentioned_legfile = LegFile.objects.get(id=mentioned_legfile_id)
                yield mentioned_legfile
            except LegFile.DoesNotExist:
                # TODO: Use a log message.
                print 'LegFile %r, referenced from key %s, does not exist!!!' % (mentioned_legfile_id, self.pk)


    def save(self, update_words=True, update_mentions=True, update_locations=True, *args, **kwargs):
        """
        Calls the default ``Models.save()`` method, and creates or updates
        metadata for the legislative file as well.

        """
        super(LegFile, self).save(*args, **kwargs)

        metadata = LegFileMetaData.objects.get_or_create(legfile=self)[0]

        if update_words:
            # Add the unique words to the metadata
            metadata.words.clear()
            unique_words = self.unique_words()
            for word in unique_words:
                md_word = MetaData_Word.objects.get_or_create(value=word)[0]
                metadata.words.add(md_word)

        if update_locations:
            # Add the unique locations to the metadata
            metadata.locations.clear()
            locations = self.addresses()
            for location in locations:
                md_location = MetaData_Location.objects.get_or_create(
                    address=location[0]
                )[0]
                metadata.locations.add(md_location)

        if update_mentions:
            # Add the mentioned files to the metadata
            metadata.mentioned_legfiles.clear()
            for mentioned_legfile in self.mentioned_legfiles():
                metadata.mentioned_legfiles.add(mentioned_legfile)

        metadata.save()


class LegFileAttachment(models.Model):
    file = models.ForeignKey(LegFile, related_name='attachments')
    description = models.CharField(max_length=1000)
    url = models.URLField()
    fulltext = models.TextField()

    class Meta:
        unique_together = (('file','url'),)


class LegAction(models.Model):
    file = models.ForeignKey(LegFile, related_name='actions')
    date_taken = models.DateField()
    description = models.CharField(max_length=1000)
    minutes = models.ForeignKey('LegMinutes', related_name='actions', null=True)
    motion = models.CharField(max_length=1000)
    acting_body = models.CharField(max_length=1000)
    notes = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (self.date_taken, self.description)

    class Meta:
        unique_together = (('file','date_taken','description','notes'),)


class LegMinutes(models.Model):
    url = models.URLField(unique=True)
    fulltext = models.TextField()
    date_taken = models.DateField(null=True)

    def __unicode__(self):
        return "(%s) %s%s" % (self.date_taken, self.fulltext[:100],
            '...' if len(self.fulltext) > 100 else '')

    @models.permalink
    def get_absolute_url(self):
        return ('minutes_detail', [str(self.pk)])

    def unique_words(self):
        """
        Gets all the white-space separated words in the minutes.  A word is
        anything that starts and ends with word characters and has no internal
        white space.

        """
        # Get rid of any punctuation on the outside of words.
        only_words = re.sub(r'(\s\W+|\W+\s|\W+$)', ' ', self.fulltext)

        # Pick out and return the unique values by spliting on whitespace, and
        # lowercasing everything.
        unique_words = set(word.lower() for word in only_words.split())
        return unique_words

    def addresses(self):
        addresses = ebdata.nlp.addresses.parse_addresses(self.fulltext)
        return addresses

    def save(self, update_words=True, *args, **kwargs):
        """
        Calls the default ``Models.save()`` method, and creates or updates
        metadata for the minutes as well.

        """
        super(LegMinutes, self).save(*args, **kwargs)

        metadata = LegMinutesMetaData.objects.get_or_create(legminutes=self)[0]

        if update_words:
            # Add the unique words to the metadata
            metadata.words.clear()
            unique_words = self.unique_words()
            for word in unique_words:
                md_word = MetaData_Word.objects.get_or_create(value=word)[0]
                metadata.words.add(md_word)

        if update_locations:
            # Add the unique locations to the metadata
            metadata.locations.clear()
            locations = self.addresses()
            for location in locations:
                md_location = MetaData_Location.objects.get_or_create(
                    address=location['address']
                )[0]
                metadata.locations.add(md_location)

        metadata.save()


#
# Meta-data
#

class LegFileMetaData (models.Model):
    legfile = models.OneToOneField('LegFile', related_name='metadata')
    words = models.ManyToManyField('MetaData_Word', related_name='references_in_legislation')
    locations = models.ManyToManyField('MetaData_Location', related_name='references_in_legislation')
    mentioned_legfiles = models.ManyToManyField('LegFile', related_name='references_in_legislation')

    def __unicode__(self):
        return (u'%s (mentions %s other files, mentioned by %s other files)' % \
            (self.legfile.pk, len(self.mentioned_legfiles.all()), len(self.legfile.references_in_legislation.all())))


class LegMinutesMetaData (models.Model):
    legminutes = models.OneToOneField('LegMinutes', related_name='metadata')
    words = models.ManyToManyField('MetaData_Word', related_name='references_in_minutes')
    locations = models.ManyToManyField('MetaData_Location', related_name='references_in_minutes')

    def __unicode__(self):
        return u'metadata for %s' % self.legminutes


class MetaData_Word (models.Model):
    value = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return '%r (used in %s files)' % (self.value, len(self.references.all()))


class MetaData_Location (models.Model):
    address = models.CharField(max_length=2048, unique=True)
    geom = models.PointField(null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '%s, Philadelphia, PA' % (self.address)

    def save(self, *args, **kwargs):
        if not self.id and not self.geom:
            self.geocode()

        super(MetaData_Location, self).save(*args, **kwargs)

    def geocode(self):
        gc = utils.geocode(self.address + ', Philadelphia, PA')
        if gc and gc['status'] == 'OK':
            x = float(gc['results'][0]['geometry']['location']['lng'])
            y = float(gc['results'][0]['geometry']['location']['lat'])
            self.geom = geos.Point(x, y)


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
