# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Shurl'
        db.create_table('shortcake_shurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('short_suffix', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True, null=True, blank=True)),
            ('access_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('shortcake', ['Shurl'])

        # Adding model 'MonthLog'
        db.create_table('shortcake_monthlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shurl', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shortcake.Shurl'])),
            ('creation_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('access_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('shortcake', ['MonthLog'])


    def backwards(self, orm):
        
        # Deleting model 'Shurl'
        db.delete_table('shortcake_shurl')

        # Deleting model 'MonthLog'
        db.delete_table('shortcake_monthlog')


    models = {
        'shortcake.monthlog': {
            'Meta': {'object_name': 'MonthLog'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shurl': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shortcake.Shurl']"})
        },
        'shortcake.shurl': {
            'Meta': {'object_name': 'Shurl'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_suffix': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['shortcake']
