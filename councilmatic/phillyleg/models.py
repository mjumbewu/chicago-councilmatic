import datetime
import ebdata.nlp.addresses
import re
import utils
import logging
from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis import geos
#from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from phillyleg.management.scraper_wrappers import PhillyLegistarSiteWrapper
from utils.models import TimestampedModelMixin

log = logging.getLogger(__name__)

#
# Metadata about the scraping process
#

class LegKeys(models.Model):
    continuation_key = models.IntegerField()


#
# Legislative File models
#

class CouncilMember(TimestampedModelMixin, models.Model):
    name = models.CharField(max_length=100)
    headshot = models.CharField(max_length=255,
        # Path to councilmember image, relative to static files dir
        default='phillyleg/noun_project_416.png')
    districts = models.ManyToManyField('CouncilDistrict', through='CouncilMemberTenure', related_name='representatives')

    NOT_YET_SET = object()
    __tenure = NOT_YET_SET
    @property
    def tenure(self):
        # Sort the tenures here instead of in a query, as there shouldn't be
        # very many, and this allows us to use prefetched tenures, if they
        # exist.
        if self.__tenure is self.NOT_YET_SET:
            tenures = sorted(self.tenures.all(), key=lambda t: t.begin)
            if tenures:
                self.__tenure = tenures[-1]
            else:
                return None
        return self.__tenure

    @property
    def district(self):
        tenure = self.tenure
        return (tenure and tenure.district)

    @property
    def is_active(self):
        tenure = self.tenure
        return (tenure is not None and tenure.end is None)

    @property
    def is_president(self):
        tenure = self.tenure
        return (tenure is not None and tenure.president)

    @property
    def is_at_large(self):
        tenure = self.tenure
        return (tenure is not None and tenure.at_large)

    def __unicode__(self):
        return self.name.lstrip("Councilmember")


class CouncilMemberTenure(TimestampedModelMixin, models.Model):
    councilmember = models.ForeignKey('CouncilMember', related_name='tenures')
    district = models.ForeignKey('CouncilDistrict', related_name='tenures', null=True, blank=True)
    at_large = models.BooleanField(default=False)
    president = models.BooleanField(default=False)
    begin = models.DateField(blank=True)
    end = models.DateField(null=True, blank=True)

    class Meta (object):
        ordering = ('-begin',)


class CouncilDistrictPlan(TimestampedModelMixin, models.Model):
    date = models.DateField()


class CouncilDistrict(TimestampedModelMixin, models.Model):
    key = models.AutoField(primary_key=True)
    id = models.IntegerField()
    shape = models.PolygonField()
    plan = models.ForeignKey('CouncilDistrictPlan', related_name='districts')

    objects = models.GeoManager()

    @property
    def representative(self):
        # Sort the tenures here instead of in a query, as there shouldn't be
        # very many, and this allows us to use prefetched tenures, if they
        # exist.
        tenures = sorted(self.tenures.all(), key=lambda t: t.begin)
        if tenures:
            return tenures[-1].councilmember

    def __unicode__(self):
        return u'District {d}'.format(d=self.id)


class LegFile(TimestampedModelMixin, models.Model):
    key = models.IntegerField(primary_key=True)
    id = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=1000, default="No contact")
    controlling_body = models.CharField(max_length=1000)
    date_scraped = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_scraped = models.DateTimeField(auto_now=True)
    final_date = models.DateField(null=True)
    intro_date = models.DateField(default=datetime.datetime.now)
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
        for action in self.actions.all().order_by('date_taken'):
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

    def topics(self)
        if 'Exemption from physical barrier' in self.title :
            return 'Physical barrier exemption'

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


    def update(self, attribs, commit=True, **save_kwargs):
        for attr, val in attribs.items():
            setattr(self, attr, val)

        if commit:
            return self.save(**save_kwargs)

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
                try:
                    md_location = MetaData_Location.objects.get_or_create(
                        address=location[0]
                    )[0]
                except MetaData_Location.CouldNotBeGeocoded:
                    continue

                metadata.locations.add(md_location)

        if update_mentions:
            # Add the mentioned files to the metadata
            metadata.mentioned_legfiles.clear()
            for mentioned_legfile in self.mentioned_legfiles():
                metadata.mentioned_legfiles.add(mentioned_legfile)

        if update_topics:
            # Add topics to the metadata
            metadata.topics.clear()
            for topic in self.topics():
                metadata.topics.add(topic)

        metadata.save()

    def get_data_source(self):
        return PhillyLegistarSiteWrapper()

    def refresh(self, stale_time=datetime.timedelta(days=1), force=False):
        """
        Update the file if it has not been updated in a while.  The "while" is
        dictated the `stale_time` parameter, a `timedelta`.  If `force` is True,
        then the refresh will happen immediately, regardless of the time it was
        last updated.
        """
        pass


class LegFileAttachment(TimestampedModelMixin, models.Model):
    file = models.ForeignKey(LegFile, related_name='attachments')
    description = models.CharField(max_length=1000)
    url = models.URLField()
    fulltext = models.TextField()

    class Meta:
        unique_together = (('file','url'),)


class LegAction(TimestampedModelMixin, models.Model):
    file = models.ForeignKey(LegFile, related_name='actions')
    date_taken = models.DateField()
    description = models.TextField()
    minutes = models.ForeignKey('LegMinutes', related_name='actions', null=True)
    motion = models.CharField(max_length=1000)
    acting_body = models.CharField(max_length=1000)
    notes = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (self.date_taken, self.description)

    class Meta:
        # TODO: Fix this; there's not actually uniqueness here.  See
        #       http://legislation.phila.gov/detailreport/?key=2915
        unique_together = (('file','date_taken','description','notes'),)
        ordering = ['date_taken']


class LegMinutes(TimestampedModelMixin, models.Model):
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

    def save(self, update_words=True, update_locations=True, *args, **kwargs):
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

class LegFileMetaData (TimestampedModelMixin, models.Model):
    legfile = models.OneToOneField('LegFile', related_name='metadata')
    words = models.ManyToManyField('MetaData_Word', related_name='references_in_legislation')
    locations = models.ManyToManyField('MetaData_Location', related_name='references_in_legislation')
    topics = models.ManyToManyField('MetaData_Topic', related_name='references_in_legislation')
    mentioned_legfiles = models.ManyToManyField('LegFile', related_name='references_in_legislation')
    
    def valid_locations(self):
        return self.locations.filter(valid=True)

    def __unicode__(self):
        return (u'%s (mentions %s other files, mentioned by %s other files)' % \
            (self.legfile.pk, len(self.mentioned_legfiles.all()), len(self.legfile.references_in_legislation.all())))


class LegMinutesMetaData (TimestampedModelMixin, models.Model):
    legminutes = models.OneToOneField('LegMinutes', related_name='metadata')
    words = models.ManyToManyField('MetaData_Word', related_name='references_in_minutes')
    locations = models.ManyToManyField('MetaData_Location', related_name='references_in_minutes')

    def __unicode__(self):
        return u'metadata for %s' % self.legminutes


class MetaData_Word (models.Model):
    value = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return '%r (used in %s files)' % (self.value, len(self.references.all()))


class MetaData_Location (TimestampedModelMixin, models.Model):
    address = models.CharField(max_length=2048, unique=True)
    geom = models.PointField(null=True)
    valid = models.BooleanField(default=True, blank=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return '{0}{1}'.format(self.address, settings.LEGISLATION['ADDRESS_SUFFIX'])

    def save(self, *args, **kwargs):
        if not self.id and not self.geom:
            self.geocode()

        super(MetaData_Location, self).save(*args, **kwargs)

    class CouldNotBeGeocoded (Exception):
        pass

    def geocode(self):
        gc = utils.geocode(self.address, settings.LEGISLATION['ADDRESS_BOUNDS'])

        if gc and gc['status'] == 'OK' and settings.LEGISLATION['ADDRESS_SUFFIX'] in gc['results'][0]['formatted_address']:
            x = float(gc['results'][0]['geometry']['location']['lng'])
            y = float(gc['results'][0]['geometry']['location']['lat'])
            self.geom = geos.Point(x, y)
        else:
            log.debug('Could not geocode the address "%s"' % self.address)
            raise self.CouldNotBeGeocoded(self.address)

class MetaData_Topic (models.Model):
    topic = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return '%r (topics: %s)' % (self.topic, len(self.references.all()))