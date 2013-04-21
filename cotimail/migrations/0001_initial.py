# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailLog'
        db.create_table(u'cotimail_emaillog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.TextField')()),
            ('pickle', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('recipients', self.gf('django.db.models.fields.TextField')()),
            ('sender', self.gf('django.db.models.fields.EmailField')(max_length=250)),
            ('reply_to', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='content_type_set_for_emaillog', to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.TextField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_sent', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'cotimail', ['EmailLog'])


    def backwards(self, orm):
        # Deleting model 'EmailLog'
        db.delete_table(u'cotimail_emaillog')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cotimail.emaillog': {
            'Meta': {'object_name': 'EmailLog'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_emaillog'", 'to': u"orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'pickle': ('django.db.models.fields.TextField', [], {}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'reply_to': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['cotimail']