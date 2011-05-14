# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CouncilMember'
        db.create_table('phillyleg_councilmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('phillyleg', ['CouncilMember'])

        # Adding model 'LegFile'
        db.create_table('phillyleg_legfile', (
            ('key', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('controlling_body', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('date_scraped', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_scraped', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('final_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('intro_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('phillyleg', ['LegFile'])

        # Adding M2M table for field sponsors on 'LegFile'
        db.create_table('phillyleg_legfile_sponsors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('legfile', models.ForeignKey(orm['phillyleg.legfile'], null=False)),
            ('councilmember', models.ForeignKey(orm['phillyleg.councilmember'], null=False))
        ))
        db.create_unique('phillyleg_legfile_sponsors', ['legfile_id', 'councilmember_id'])

        # Adding model 'LegFileAttachment'
        db.create_table('phillyleg_legfileattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phillyleg.LegFile'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('phillyleg', ['LegFileAttachment'])

        # Adding unique constraint on 'LegFileAttachment', fields ['file', 'url']
        db.create_unique('phillyleg_legfileattachment', ['file_id', 'url'])

        # Adding model 'LegAction'
        db.create_table('phillyleg_legaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phillyleg.LegFile'])),
            ('date_taken', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('minutes_url', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('motion', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('acting_body', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('phillyleg', ['LegAction'])

        # Adding unique constraint on 'LegAction', fields ['file', 'date_taken', 'description', 'notes']
        db.create_unique('phillyleg_legaction', ['file_id', 'date_taken', 'description', 'notes'])

        # Adding model 'Subscription'
        db.create_table('phillyleg_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_sent', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('phillyleg', ['Subscription'])

        # Adding model 'KeywordSubscription'
        db.create_table('phillyleg_keywordsubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(related_name='keywords', to=orm['phillyleg.Subscription'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('phillyleg', ['KeywordSubscription'])

        # Adding model 'CouncilMemberSubscription'
        db.create_table('phillyleg_councilmembersubscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(related_name='councilmembers', to=orm['phillyleg.Subscription'])),
            ('councilmember', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['phillyleg.CouncilMember'])),
        ))
        db.send_create_signal('phillyleg', ['CouncilMemberSubscription'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'LegAction', fields ['file', 'date_taken', 'description', 'notes']
        db.delete_unique('phillyleg_legaction', ['file_id', 'date_taken', 'description', 'notes'])

        # Removing unique constraint on 'LegFileAttachment', fields ['file', 'url']
        db.delete_unique('phillyleg_legfileattachment', ['file_id', 'url'])

        # Deleting model 'CouncilMember'
        db.delete_table('phillyleg_councilmember')

        # Deleting model 'LegFile'
        db.delete_table('phillyleg_legfile')

        # Removing M2M table for field sponsors on 'LegFile'
        db.delete_table('phillyleg_legfile_sponsors')

        # Deleting model 'LegFileAttachment'
        db.delete_table('phillyleg_legfileattachment')

        # Deleting model 'LegAction'
        db.delete_table('phillyleg_legaction')

        # Deleting model 'Subscription'
        db.delete_table('phillyleg_subscription')

        # Deleting model 'KeywordSubscription'
        db.delete_table('phillyleg_keywordsubscription')

        # Deleting model 'CouncilMemberSubscription'
        db.delete_table('phillyleg_councilmembersubscription')


    models = {
        'phillyleg.councilmember': {
            'Meta': {'object_name': 'CouncilMember'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'phillyleg.councilmembersubscription': {
            'Meta': {'object_name': 'CouncilMemberSubscription'},
            'councilmember': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.CouncilMember']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'councilmembers'", 'to': "orm['phillyleg.Subscription']"})
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
            'date_taken': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.LegFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes_url': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'motion': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        },
        'phillyleg.legfile': {
            'Meta': {'object_name': 'LegFile'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'controlling_body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'intro_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['phillyleg.CouncilMember']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'phillyleg.legfileattachment': {
            'Meta': {'unique_together': "(('file', 'url'),)", 'object_name': 'LegFileAttachment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.LegFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        'phillyleg.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['phillyleg']
