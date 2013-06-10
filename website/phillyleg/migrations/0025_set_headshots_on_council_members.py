# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        green = orm.CouncilMember.objects.get_or_create(name='Councilmember Green')[0]
        green.headshot = 'phillyleg/billGreenSM.jpg'
        green.save()
        
        oniell = orm.CouncilMember.objects.get_or_create(name='Councilmember O\'Neill')[0]
        oniell.headshot = 'phillyleg/Councilman_ONeillsmall.gif'
        oniell.save()
        
        kelly = orm.CouncilMember.objects.get_or_create(name='Councilmember Kelly')[0]
        kelly.headshot = 'phillyleg/jackKellySM.jpg'
        kelly.save()
        
        tasco = orm.CouncilMember.objects.get_or_create(name='Councilmember Tasco')[0]
        tasco.headshot = 'phillyleg/TascoSM.jpg'
        tasco.save()
        
        rb = orm.CouncilMember.objects.get_or_create(name='Councilmember Reynolds Brown')[0]
        rb.headshot = 'phillyleg/BRBphoto_SM.jpg'
        rb.save()
        
        dicicco = orm.CouncilMember.objects.get_or_create(name='Councilmember DiCicco')[0]
        dicicco.headshot = 'phillyleg/DiCiccoSM.jpg'
        dicicco.save()
        
        blackwell = orm.CouncilMember.objects.get_or_create(name='Councilmember Blackwell')[0]
        blackwell.headshot = 'phillyleg/JBlackwellSM.jpg'
        blackwell.save()
        
        verna = orm.CouncilMember.objects.get_or_create(name='Council President Verna')[0]
        verna.headshot = 'phillyleg/VernaSM.jpg'
        verna.save()
        
        jones = orm.CouncilMember.objects.get_or_create(name='Councilmember Jones')[0]
        jones.headshot = 'phillyleg/cJonesSM.jpg'
        jones.save()
        
        miller = orm.CouncilMember.objects.get_or_create(name='Councilmember Miller')[0]
        miller.headshot = 'phillyleg/drmSM.jpg'
        miller.save()
        
        kenny = orm.CouncilMember.objects.get_or_create(name='Councilmember Kenney')[0]
        kenny.headshot = 'phillyleg/JimKennySM.jpg'
        kenny.save()
        
        quinones = orm.CouncilMember.objects.get_or_create(name='Councilmember Sanchez')[0]
        quinones.headshot = 'phillyleg/MDQSSM.jpg'
        quinones.save()
        
        clarke = orm.CouncilMember.objects.get_or_create(name='Councilmember Clarke')[0]
        clarke.headshot = 'phillyleg/ClarkeSM.jpg'
        clarke.save()
        
        goode = orm.CouncilMember.objects.get_or_create(name='Councilmember Goode')[0]
        goode.headshot = 'phillyleg/GoodeSM.jpg'
        goode.save()
        
        krajewski = orm.CouncilMember.objects.get_or_create(name='Councilmember Krajewski')[0]
        krajewski.headshot = 'phillyleg/KrajewskiSM.jpg'
        krajewski.save()
        
        rizzo = orm.CouncilMember.objects.get_or_create(name='Councilmember Rizzo')[0]
        rizzo.headshot = 'phillyleg/RizzoSM.jpg'
        rizzo.save()
        
        greenlee = orm.CouncilMember.objects.get_or_create(name='Councilmember Greenlee')[0]
        greenlee.headshot = 'phillyleg/williamGreenleeSM.jpg'
        greenlee.save()


    def backwards(self, orm):
        "Write your backwards methods here."


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'phillyleg.councilmember': {
            'Meta': {'object_name': 'CouncilMember'},
            'headshot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
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
            'date_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.LegFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.LegMinutes']", 'null': 'True'}),
            'motion': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        },
        'phillyleg.legfile': {
            'Meta': {'object_name': 'LegFile'},
            'bookmarks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'bookmarks'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'controlling_body': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'date_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'final_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'intro_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'key': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['phillyleg.CouncilMember']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'phillyleg.legfileattachment': {
            'Meta': {'unique_together': "(('file', 'url'),)", 'object_name': 'LegFileAttachment'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['phillyleg.LegFile']"}),
            'fulltext': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'})
        },
        'phillyleg.legfilemetadata': {
            'Meta': {'object_name': 'LegFileMetaData'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legfile': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata'", 'unique': 'True', 'to': "orm['phillyleg.LegFile']"}),
            'mentioned_legfiles': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references'", 'symmetrical': 'False', 'to': "orm['phillyleg.LegFile']"}),
            'words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'references'", 'symmetrical': 'False', 'to': "orm['phillyleg.MetaData_Word']"})
        },
        'phillyleg.legminutes': {
            'Meta': {'object_name': 'LegMinutes'},
            'date_taken': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'fulltext': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2048'})
        },
        'phillyleg.metadata_word': {
            'Meta': {'object_name': 'MetaData_Word'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'phillyleg.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['phillyleg']
