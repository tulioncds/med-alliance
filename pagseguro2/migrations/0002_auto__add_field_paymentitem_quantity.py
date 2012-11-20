# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'PaymentItem.quantity'
        db.add_column('pagseguro2_paymentitem', 'quantity', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'PaymentItem.quantity'
        db.delete_column('pagseguro2_paymentitem', 'quantity')


    models = {
        'pagseguro2.notification': {
            'Meta': {'object_name': 'Notification'},
            'checked': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'pagseguro2.payment': {
            'Meta': {'object_name': 'Payment'},
            'answered_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pagseguro2.PaymentItem']", 'symmetrical': 'False'}),
            'payment_method_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'payment_method_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'pagseguro2.paymentitem': {
            'Meta': {'object_name': 'PaymentItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pagseguro2']
