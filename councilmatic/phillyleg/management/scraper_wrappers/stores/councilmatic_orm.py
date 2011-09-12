import datetime
import phillyleg

import phillyleg.management.scraperwiki as scraperwiki
from phillyleg.models import \
    LegFile, LegFileAttachment, LegAction, LegMinutes, CouncilMember

class CouncilmaticDataStoreWrapper (object):
    """
    This is the interface over an arbitrary database where the information is
    being stored.  I'm using it primarily because I want the scraper code to be
    used on both ScraperWiki and in my Django app on my Django models.  For my
    app, I want local access to the data.  But I love ScraperWiki as a central
    place where you can find data about anything you want, so it's important to
    have the data available on SW as well.
    """
    def get_latest_key(self):
        '''Check the datastore for the key of the most recent filing.'''

        records = LegFile.objects.order_by('-key')
        try:
            return records[0].key
        except IndexError:
            return STARTING_KEY

    def save_legis_file(self, file_record, attachment_records,
                        action_records, minutes_records):
        """
        Take a legislative file record and do whatever needs to be
        done to get it into the database.
        """
        file_record = self.__convert_or_delete_date(file_record, 'intro_date')
        file_record = self.__convert_or_delete_date(file_record, 'final_date')

        # Don't include the sponsors list, as the model framework doesn't allow
        # batch inserting of lists for a ManyToManyField, and we will need to
        # insert each sponsor individually.  See below in 'Create the record'.
        sponsor_names = file_record['sponsors']
        del file_record['sponsors']

        # Create the record
        legfile = LegFile(**file_record)
        legfile.save()
        for sponsor_name in sponsor_names.split(','):
            sponsor_name = sponsor_name.strip()
            sponsor = CouncilMember.objects.get_or_create(name=sponsor_name)[0]
            legfile.sponsors.add(sponsor)
        legfile.save()

        # Create notes attached to the record
        for attachment_record in attachment_records:
            attachment_record = self.__replace_key_with_legfile(attachment_record)
            self.__save_or_ignore(LegFileAttachment, attachment_record)

        # Create minutes
        for minutes_record in minutes_records:
            self.__save_or_ignore(LegMinutes, minutes_record)

        # Create actions attached to the record
        for action_record in action_records:
            action_record = self.__replace_key_with_legfile(action_record)
            action_record = self.__replace_url_with_minutes(action_record)
            self.__save_or_ignore(LegAction, action_record)

    def __convert_or_delete_date(self, file_record, date_key):
        if file_record[date_key]:
            pass
#            file_record[date_key] = datetime.datetime.strptime(
#                file_record[date_key], '%m/%d/%Y')
        else:
            del file_record[date_key]

        return file_record

    def __replace_key_with_legfile(self, record):
        legfile = LegFile.objects.get(key=record['key'])
        del record['key']
        record['file'] = legfile

        return record

    def __replace_url_with_minutes(self, record):
        minutes_url = record['minutes_url']

        if minutes_url == '':
            minutes = None
        else:
            try:
                minutes = LegMinutes.objects.get(url=record['minutes_url'])
            except phillyleg.models.LegMinutes.DoesNotExist:
                minutes = None

        del record['minutes_url']
        record['minutes'] = minutes

        return record

    def __save_or_ignore(self, ModelClass, record):
        model_instance = ModelClass(**record)
        try:
            model_instance.save()
            return True
        except:
            # If it's a duplicate, don't worry about it.  Just move on.
            return False
