# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentItem'
        db.create_table('pagseguro2_paymentitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
        ))
        db.send_create_signal('pagseguro2', ['PaymentItem'])

        # Adding model 'Payment'
        db.create_table('pagseguro2_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('answered_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('payment_method_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('payment_method_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('pagseguro2', ['Payment'])

        # Adding M2M table for field payment_items on 'Payment'
        db.create_table('pagseguro2_payment_payment_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payment', models.ForeignKey(orm['pagseguro2.payment'], null=False)),
            ('paymentitem', models.ForeignKey(orm['pagseguro2.paymentitem'], null=False))
        ))
        db.create_unique('pagseguro2_payment_payment_items', ['payment_id', 'paymentitem_id'])

        # Adding model 'Notification'
        db.create_table('pagseguro2_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=39)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('received_on', self.gf('django.db.models.fields.DateTimeField')()),
            ('checked', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('pagseguro2', ['Notification'])


    def backwards(self, orm):
        
        # Deleting model 'PaymentItem'
        db.delete_table('pagseguro2_paymentitem')

        # Deleting model 'Payment'
        db.delete_table('pagseguro2_payment')

        # Removing M2M table for field payment_items on 'Payment'
        db.delete_table('pagseguro2_payment_payment_items')

        # Deleting model 'Notification'
        db.delete_table('pagseguro2_notification')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pagseguro2']
