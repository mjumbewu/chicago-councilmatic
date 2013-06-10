# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CouncilMember.created_datetime'
        db.add_column('phillyleg_councilmember', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilMember.updated_datetime'
        db.add_column('phillyleg_councilmember', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'MetaData_Location.created_datetime'
        db.add_column('phillyleg_metadata_location', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'MetaData_Location.updated_datetime'
        db.add_column('phillyleg_metadata_location', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFile.created_datetime'
        db.add_column('phillyleg_legfile', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFile.updated_datetime'
        db.add_column('phillyleg_legfile', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegAction.created_datetime'
        db.add_column('phillyleg_legaction', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegAction.updated_datetime'
        db.add_column('phillyleg_legaction', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilDistrictPlan.created_datetime'
        db.add_column('phillyleg_councildistrictplan', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilDistrictPlan.updated_datetime'
        db.add_column('phillyleg_councildistrictplan', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFileMetaData.created_datetime'
        db.add_column('phillyleg_legfilemetadata', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFileMetaData.updated_datetime'
        db.add_column('phillyleg_legfilemetadata', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFileAttachment.created_datetime'
        db.add_column('phillyleg_legfileattachment', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegFileAttachment.updated_datetime'
        db.add_column('phillyleg_legfileattachment', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegMinutes.created_datetime'
        db.add_column('phillyleg_legminutes', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegMinutes.updated_datetime'
        db.add_column('phillyleg_legminutes', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegMinutesMetaData.created_datetime'
        db.add_column('phillyleg_legminutesmetadata', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'LegMinutesMetaData.updated_datetime'
        db.add_column('phillyleg_legminutesmetadata', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilMemberTenure.created_datetime'
        db.add_column('phillyleg_councilmembertenure', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilMemberTenure.updated_datetime'
        db.add_column('phillyleg_councilmembertenure', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilDistrict.created_datetime'
        db.add_column('phillyleg_councildistrict', 'created_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'CouncilDistrict.updated_datetime'
        db.add_column('phillyleg_councildistrict', 'updated_datetime',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2012, 4, 30, 0, 0), blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'CouncilMember.created_datetime'
        db.delete_column('phillyleg_councilmember', 'created_datetime')

        # Deleting field 'CouncilMember.updated_datetime'
        db.delete_column('phillyleg_councilmember', 'updated_datetime')

        # Deleting field 'MetaData_Location.created_datetime'
        db.delete_column('phillyleg_metadata_location', 'created_datetime')

        # Deleting field 'MetaData_Location.updated_datetime'
        db.delete_column('phillyleg_metadata_location', 'updated_datetime')

        # Deleting field 'LegFile.created_datetime'
        db.delete_column('phillyleg_legfile', 'created_datetime')

        # Deleting field 'LegFile.updated_datetime'
        db.delete_column('phillyleg_legfile', 'updated_datetime')

        # Deleting field 'LegAction.created_datetime'
        db.delete_column('phillyleg_legaction', 'created_datetime')

        # Deleting field 'LegAction.updated_datetime'
        db.delete_column('phillyleg_legaction', 'updated_datetime')

        # Deleting field 'CouncilDistrictPlan.created_datetime'
        db.delete_column('phillyleg_councildistrictplan', 'created_datetime')

        # Deleting field 'CouncilDistrictPlan.updated_datetime'
        db.delete_column('phillyleg_councildistrictplan', 'updated_datetime')

        # Deleting field 'LegFileMetaData.created_datetime'
        db.delete_column('phillyleg_legfilemetadata', 'created_datetime')

        # Deleting field 'LegFileMetaData.updated_datetime'
        db.delete_column('phillyleg_legfilemetadata', 'updated_datetime')

        # Deleting field 'LegFileAttachment.created_datetime'
        db.delete_column('phillyleg_legfileattachment', 'created_datetime')

        # Deleting field 'LegFileAttachment.updated_datetime'
        db.delete_column('phillyleg_legfileattachment', 'updated_datetime')

        # Deleting field 'LegMinutes.created_datetime'
        db.delete_column('phillyleg_legminutes', 'created_datetime')

        # Deleting field 'LegMinutes.updated_datetime'
        db.delete_column('phillyleg_legminutes', 'updated_datetime')

        # Deleting field 'LegMinutesMetaData.created_datetime'
        db.delete_column('phillyleg_legminutesmetadata', 'created_datetime')

        # Deleting field 'LegMinutesMetaData.updated_datetime'
        db.delete_column('phillyleg_legminutesmetadata', 'updated_datetime')

        # Deleting field 'CouncilMemberTenure.created_datetime'
        db.delete_column('phillyleg_councilmembertenure', 'created_datetime')

        # Deleting field 'CouncilMemberTenure.updated_datetime'
        db.delete_column('phillyleg_councilmembertenure', 'updated_datetime')

        # Deleting field 'CouncilDistrict.created_datetime'
        db.delete_column('phillyleg_councildistrict', 'created_datetime')

        # Deleting field 'CouncilDistrict.updated_datetime'
        db.delete_column('phillyleg_councildistrict', 'updated_datetime')

    models = {
        'phillyleg.councildistrict': {
            'Meta': {'object_name': 'CouncilDistrict'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {}),
            'key': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.CouncilDistrictPlan']"}),
            'shape': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.councildistrictplan': {
            'Meta': {'object_name': 'CouncilDistrictPlan'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.councilmember': {
            'Meta': {'object_name': 'CouncilMember'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'districts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'representatives'", 'symmetrical': 'False', 'through': "orm['phillyleg.CouncilMemberTenure']", 'to': "orm['phillyleg.CouncilDistrict']"}),
            'headshot': ('django.db.models.fields.CharField', [], {'default': "'phillyleg/noun_project_416.png'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.councilmembersubscription': {
            'Meta': {'object_name': 'CouncilMemberSubscription'},
            'councilmember': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.CouncilMember']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'councilmembers'", 'to': "orm['phillyleg.Subscription']"})
        },
        'phillyleg.councilmembertenure': {
            'Meta': {'object_name': 'CouncilMemberTenure'},
            'at_large': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'begin': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'councilmember': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tenures'", 'to': "orm['phillyleg.CouncilMember']"}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tenures'", 'null': 'True', 'to': "orm['phillyleg.CouncilDistrict']"}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'president': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.keywordsubscription': {
            'Meta': {'object_name': 'KeywordSubscription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'keywords'", 'to': "orm['phillyleg.Subscription']"})
        },
        'phillyleg.legaction': {
            'Meta': {'unique_together': "(('file', 'date_taken', 'description', 'notes'),)", 'object_name': 'LegAction'},
            'acting_body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': "orm['phillyleg.LegFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'null': 'True', 'to': "orm['phillyleg.LegMinutes']"}),
            'motion': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.legfile': {
            'Meta': {'ordering': "['-key']", 'object_name': 'LegFile'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'controlling_body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'intro_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'legislation'", 'symmetrical': 'False', 'to': "orm['phillyleg.CouncilMember']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'phillyleg.legfileattachment': {
            'Meta': {'unique_together': "(('file', 'url'),)", 'object_name': 'LegFileAttachment'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['phillyleg.LegFile']"}),
            'fulltext': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'phillyleg.legfilemetadata': {
            'Meta': {'object_name': 'LegFileMetaData'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legfile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata'", 'unique': 'True', 'to': "orm['phillyleg.LegFile']"}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references_in_legislation'", 'symmetrical': 'False', 'to': "orm['phillyleg.MetaData_Location']"}),
            'mentioned_legfiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references_in_legislation'", 'symmetrical': 'False', 'to': "orm['phillyleg.LegFile']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references_in_legislation'", 'symmetrical': 'False', 'to': "orm['phillyleg.MetaData_Word']"})
        },
        'phillyleg.legkeys': {
            'Meta': {'object_name': 'LegKeys'},
            'continuation_key': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'phillyleg.legminutes': {
            'Meta': {'object_name': 'LegMinutes'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fulltext': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'phillyleg.legminutesmetadata': {
            'Meta': {'object_name': 'LegMinutesMetaData'},
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legminutes': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata'", 'unique': 'True', 'to': "orm['phillyleg.LegMinutes']"}),
            'locations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references_in_minutes'", 'symmetrical': 'False', 'to': "orm['phillyleg.MetaData_Location']"}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references_in_minutes'", 'symmetrical': 'False', 'to': "orm['phillyleg.MetaData_Word']"})
        },
        'phillyleg.metadata_location': {
            'Meta': {'object_name': 'MetaData_Location'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'}),
            'created_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'phillyleg.metadata_word': {
            'Meta': {'object_name': 'MetaData_Word'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'phillyleg.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['phillyleg']