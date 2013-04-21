# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EmailLog.pickle'
        db.delete_column(u'cotimail_emaillog', 'pickle')

        # Adding field 'EmailLog.pickled_data'
        db.add_column(u'cotimail_emaillog', 'pickled_data',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'EmailLog.pickle'
        db.add_column(u'cotimail_emaillog', 'pickle',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'EmailLog.pickled_data'
        db.delete_column(u'cotimail_emaillog', 'pickled_data')


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
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'content_type_set_for_emaillog'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'object_pk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pickled_data': ('django.db.models.fields.TextField', [], {}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'reply_to': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'sender': ('django.db.models.fields.EmailField', [], {'max_length': '250'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['cotimail']