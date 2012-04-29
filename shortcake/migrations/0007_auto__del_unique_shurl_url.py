# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Removing unique constraint on 'Shurl', fields ['url']
        db.delete_unique('shortcake_shurl', ['url'])


    def backwards(self, orm):
        
        # Adding unique constraint on 'Shurl', fields ['url']
        db.create_unique('shortcake_shurl', ['url'])


    models = {
        'shortcake.domain': {
            'Meta': {'object_name': 'Domain'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'domain': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'shortcake.monthlog': {
            'Meta': {'ordering': "['month']", 'object_name': 'MonthLog'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shortcake.Domain']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.DateField', [], {'default': 'datetime.date(2012, 4, 1)'})
        },
        'shortcake.shurl': {
            'Meta': {'ordering': "['-creation_time']", 'object_name': 'Shurl'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_suffix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['shortcake']
