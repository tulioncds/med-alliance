# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentPaymentItemRel'
        db.create_table('pagseguro2_paymentpaymentitemrel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paymentitem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagseguro2.PaymentItem'])),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pagseguro2.Payment'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('pagseguro2', ['PaymentPaymentItemRel'])

        # Adding model 'Transaction'
        db.create_table('pagseguro2_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gross_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('discount_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('fee_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('net_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('extra_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=2)),
            ('installment_count', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('pagseguro2', ['Transaction'])

        # Deleting field 'PaymentItem.quantity'
        db.delete_column('pagseguro2_paymentitem', 'quantity')

        # Deleting field 'Payment.status'
        db.delete_column('pagseguro2_payment', 'status')

        # Deleting field 'Payment.transaction_code'
        db.delete_column('pagseguro2_payment', 'transaction_code')

        # Deleting field 'Payment.transaction_date'
        db.delete_column('pagseguro2_payment', 'transaction_date')

        # Adding field 'Payment.reference'
        db.add_column('pagseguro2_payment', 'reference', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True, null=True, blank=True), keep_default=False)

        # Removing M2M table for field payment_items on 'Payment'
        db.delete_table('pagseguro2_payment_payment_items')


    def backwards(self, orm):
        
        # Deleting model 'PaymentPaymentItemRel'
        db.delete_table('pagseguro2_paymentpaymentitemrel')

        # Deleting model 'Transaction'
        db.delete_table('pagseguro2_transaction')

        # Adding field 'PaymentItem.quantity'
        db.add_column('pagseguro2_paymentitem', 'quantity', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'Payment.status'
        db.add_column('pagseguro2_payment', 'status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Payment.transaction_code'
        db.add_column('pagseguro2_payment', 'transaction_code', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True), keep_default=False)

        # Adding field 'Payment.transaction_date'
        db.add_column('pagseguro2_payment', 'transaction_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Payment.reference'
        db.delete_column('pagseguro2_payment', 'reference')

        # Adding M2M table for field payment_items on 'Payment'
        db.create_table('pagseguro2_payment_payment_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payment', models.ForeignKey(orm['pagseguro2.payment'], null=False)),
            ('paymentitem', models.ForeignKey(orm['pagseguro2.paymentitem'], null=False))
        ))
        db.create_unique('pagseguro2_payment_payment_items', ['payment_id', 'paymentitem_id'])


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
        'pagseguro2.notification': {
            'Meta': {'object_name': 'Notification'},
            'checked': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '39'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'pagseguro2.payment': {
            'Meta': {'object_name': 'Payment'},
            'answered_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_items': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['pagseguro2.PaymentItem']", 'through': "orm['pagseguro2.PaymentPaymentItemRel']", 'symmetrical': 'False'}),
            'payment_method_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'payment_method_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'pagseguro2.paymentitem': {
            'Meta': {'object_name': 'PaymentItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'pagseguro2.paymentpaymentitemrel': {
            'Meta': {'object_name': 'PaymentPaymentItemRel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagseguro2.Payment']"}),
            'paymentitem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pagseguro2.PaymentItem']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'pagseguro2.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'discount_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'extra_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'fee_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'gross_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installment_count': ('django.db.models.fields.IntegerField', [], {}),
            'net_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '2'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['pagseguro2']
