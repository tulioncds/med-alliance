#coding: utf-8

from xml.dom.minidom import Document

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

import unicodedata
import api
import choices
import datetime
import configs
from xmlreader import document2dict
from xmlreader import errors_to_list
from django.core.exceptions import ValidationError
from pagseguro2.configs import PAGSEGURO_CLIENT_PAYMENT_REDIRECT_URL, PAGSEGURO_DATETIME_FORMAT
import urllib
from decimal import Decimal


class Item(models.Model):
    '''
        One of the many possible items in a Payment
    '''
    
    description = models.CharField(max_length=100, verbose_name=u"Description")
    amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name=u"Unit price")

    class Meta():
        verbose_name = u"Item"
        verbose_name_plural = u"Items"
        
    def __unicode__(self):
        return "%d: %s" % (self.id, self.description)
    
    def to_element(self, document):
        '''
            Returns the xml.dom.minidom.Element version of self into document parameter.
        '''
        item = document.createElement("item")
        
        id = document.createElement("id")
        id.appendChild(document.createTextNode(str(self.id)))
        item.appendChild(id)
        description = document.createElement("description")
        description.appendChild(document.createTextNode(unicodedata.normalize('NFKD', self.description).encode('ascii', 'ignore')))
        item.appendChild(description)
        
        amount = document.createElement("amount")
        amount.appendChild(document.createTextNode(str(self.amount)))
        item.appendChild(amount)
                
        return item

class PaymentItemRel(models.Model):
    '''
        Relation between Payment and its Items.
    '''
    item = models.ForeignKey(Item, verbose_name=u"Item")
    payment = models.ForeignKey('Payment', verbose_name=u"Payment")
    quantity = models.IntegerField(default=1, verbose_name=u"Quantity")

    class Meta():
        verbose_name = u"'Payment - Item' Relation"
        verbose_name_plural = u"'Payment - Item' Relations"
        
    def __unicode__(self):
        return u"%d: %s, (%s|%s)" % (self.id, self.item, self.payment, self.quantity)
    
    def to_element(self, document):
        '''
            Returns the xml.dom.minidom.Element version of self into document parameter
            based on the Item.to_element.
        '''
        item = self.item.to_element(document)
        
        quantity = document.createElement("quantity")
        quantity.appendChild(document.createTextNode(str(self.quantity)))
        item.appendChild(quantity)
               
        return item
    
    
class Payment(models.Model):
    '''
        Representation for payment instances inside the PagSeguro system.
    '''
  
    user = models.ForeignKey(User, verbose_name=u"User")
    code = models.CharField(max_length=32, null=True, blank=True, unique=True, verbose_name=u"Identification code")
    reference = models.CharField(max_length=200, null=True, blank=True, unique=True, verbose_name=u"Reference")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=u"Created on")
    answered_on = models.DateTimeField(null=True, blank=True, verbose_name=u"Answered on")
    method_type = models.IntegerField(null=True, blank=True, choices=choices.PAYMENT_METHOD_TYPE_CHOICES, verbose_name=u"Payment method type")
    method_code = models.IntegerField(null=True, blank=True, choices=choices.PAYMENT_METHOD_CODE_CHOICES, verbose_name=u"Payment method code")
    items = models.ManyToManyField(Item, through=PaymentItemRel, verbose_name=u"Payment items")

    class Meta():
        verbose_name = u"Payment"
        verbose_name_plural = u"Payments"
        
    def __unicode__(self):
        return "%d: %s" % (self.id, self.code if self.code else u"Sem código")
             
    @property
    def transactions(self):
        return Transaction.objects.filter(reference=self.reference)
    
    def to_element(self, document, redirect_url=settings.PAGSEGURO_DEFAULT_REDIRECT_URL):
        '''
            Returns the xml.dom.minidom.Document version of self.
            The redirect_url parameter is used as the value of the xml.dom.Element in the document.
        '''
        container = document.createElement("checkout")
        
        currency = document.createElement("currency")
        currency.appendChild(document.createTextNode(str(configs.PAGSEGURO_CURRENCY)))
        container.appendChild(currency)
        
        reference = document.createElement("reference")
        reference.appendChild(document.createTextNode(str(self.reference)))
        container.appendChild(reference)
        
        redirect = document.createElement("redirectURL")
        redirect.appendChild(document.createTextNode(str(redirect_url)))
        container.appendChild(redirect)
        
        items = document.createElement("items")
        container.appendChild(items)
        
        #Iterating over the items to fill the items element
        for payment_item_rel in self.paymentitemrel_set.all():
            items.appendChild(payment_item_rel.to_element(document))
        
        return container
    
    
    def submit(self, redirect_url):
        '''
            Sends self as a Payment through PagSeguro API.
            Payment instance MUST BE SAVED before calling this method.
        '''
        
        if not self.id:
            #Temporary to identify which problem caused the crash.
            raise ValidationError
        
        #creating a reference if its None
        if self.reference is None:
            self.reference = configs.PAGSEGURO_REFERENCE_PREFIX + str(self.id)

        document = Document()
        document.appendChild(self.to_element(document, redirect_url))
        
        response = document2dict(api.submit_payment(document))
  
        try:
            self.code = response['checkout']['code']
            self.answered_on = datetime.datetime.now()
            self.save()
        except:
            error_str = ""
            if type(response["errors"]["error"]) != list:
                response["errors"]["error"] = [response["errors"]["error"]]
            for error in response["errors"]["error"]:
                error_payment = ErrorPayment()
                error_payment.code = int(error['code'])
                error_payment.payment = self
                error_payment.save()
                error_str += "[%s: %s]" % (error_payment.code,
                                           error_payment.get_code_display())
            raise Exception(error_str)
        
    @property
    def client_url(self):
        return PAGSEGURO_CLIENT_PAYMENT_REDIRECT_URL % urllib.urlencode({'code': self.code})
    
    def add_item(self, item, quantity):
        PaymentItemRel(item=item, payment=self, quantity=quantity).save()
        
 
class Transaction(models.Model):
    '''
        Representation for transaction instances inside the PagSeguro system.
    '''
        
    code = models.CharField(max_length=36, null=True, blank=True, unique=True, verbose_name=u"Code")
    reference = models.CharField(max_length=200, null=True, blank=True, verbose_name=u"Payment Reference")
    type = models.IntegerField(null=True, blank=True, choices=choices.TYPE_CHOICES, verbose_name=u"Type")
    status = models.IntegerField(null=True, blank=True, choices=choices.STATUS_CHOICES, verbose_name=u"Status")
    
    gross_amount = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=u"Gross Amount")
    discount_amount = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=u"Discount Amount")
    fee_amount = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=u"Fee Amount")
    net_amount = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=u"Net Amount")
    extra_amount = models.DecimalField(null=True, blank=True,max_digits=11, decimal_places=2, verbose_name=u"Extra Amount")
    
    installment_count = models.IntegerField(null=True, blank=True,verbose_name=u"Installment Count")
    
    date = models.DateTimeField(null=True, blank=True, verbose_name=u"Date")
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=u"Created on")

    class Meta():
        verbose_name = u"Transaction"
        verbose_name_plural = u"Transactions"
        
    def __init__(self, *args, **kwargs):
        response = kwargs.pop('response', None)
        super(Transaction, self).__init__(*args, **kwargs)
        if response is not None:
            self.parse(response)
            
    def parse(self, transaction_dict):
        self.reference = transaction_dict['reference']
        self.code = transaction_dict['code']
        self.type = int(transaction_dict['type'])
        self.status = int(transaction_dict['status'])
        self.gross_amount = transaction_dict['grossAmount']
        self.discount_amount = transaction_dict['discountAmount']
        self.fee_amount = transaction_dict['feeAmount']
        self.net_amount = transaction_dict['netAmount']
        self.extra_amount = transaction_dict['extraAmount']
        self.installment_count = int(transaction_dict.get('installmentCount', 1))
        self.date = datetime.datetime.strptime(transaction_dict['date'].split('.')[0], #ignoring milliseconds and timezone
                                               PAGSEGURO_DATETIME_FORMAT)
        
    def __unicode__(self):
        return "%d: %s" % (self.id, self.code)
    

    def check(self):
        response = document2dict(api.check_transaction(self.code))
        self.parse(response['transaction'])
        # override to get the last event of the transaction on pagseguro
        self.date = datetime.datetime.strptime(response['transaction']['lastEventDate'].split('.')[0], PAGSEGURO_DATETIME_FORMAT)
        self.save()

    def get_user(self):
        payment = Payment.objects.get(reference=self.reference)
        return  '<a href="%s">%s</a>' % (payment.user.get_absolute_url(), payment.user.username)
    get_user.short_description = U"Usuário"
    get_user.allow_tags = True

    @property
    def payments(self):
        return Payment.objects.filter(reference=self.reference)
    
    @classmethod
    def query(cls, initial_date, final_date, page=None,
                       max_page_results=None):
        '''
            A wrapper to api.query_transactions that converst the result into dict
            using xmlreader.document2dict
        '''
        return document2dict(api.query_transactions(initial_date, final_date,
                                                    page, max_page_results))
    
class Notification(models.Model):
    '''
        Notification returnd by the PagSeguro system when a status change on any payment is detected.
    '''

    code = models.CharField(max_length=39, unique=True, verbose_name=u"Identification code")
    type = models.IntegerField(choices=choices.TYPE_CHOICES, default=choices.TYPE_TRANSACTION[0], verbose_name=u"Type")
    received_on = models.DateTimeField(auto_now_add=True, verbose_name=u"Received on")
    checked = models.IntegerField(choices=choices.CHECKED_CHOICES, default=choices.CHECKED_NO[0], verbose_name=u"Checking status")
    
    class Meta():
        verbose_name = u"Notification"
        verbose_name_plural = u"Notifications"
        
    def __unicode__(self):
        return "%d: %s" % (self.id, self.code)
    
    def check(self):
        response = document2dict(api.check_notification(self.code))
        try:
            transaction = Transaction(response=response['transaction'])
            transaction.save()
            
            payment = Payment.objects.get(reference=transaction.reference)
            payment.method_type = int(response['transaction']['paymentMethod']['type'])
            payment.method_code = int(response['transaction']['paymentMethod']['code'])
            payment.save()
            
            self.checked = choices.CHECKED_YES_SUCCESS[0]
            self.save()
        except:
            error_str = ""
            if type(response["errors"]["error"]) != list:
                response["errors"]["error"] = [response["errors"]["error"]]
            for error in response["errors"]["error"]:
                error_payment = ErrorNotification()
                error_payment.code = int(error['code'])
                error_payment.notification = self
                error_payment.save()
                error_str += "[%s: %s]" % (error_payment.code,
                                           error_payment.get_code_display())
                
            self.checked = choices.CHECKED_YES_FAILURE[0]
            self.save()
            raise Exception(error_str)
        
    

class Error(models.Model):
    '''
        Represents the possible errors returned by the various consults and submitions 
        to the PagSeguro System.
    '''
    
    code = models.IntegerField(choices=choices.ERROR_CHOICES, verbose_name=u'Code')
    date = models.DateTimeField(auto_now_add=True, verbose_name=u'Received on')
    
    class Meta():
        abstract = True
        verbose_name = u"Error"
        verbose_name_plural = u"Errors"
        
    def __unicode__(self):
        return "%d: %d" % (self.id, self.code)
    

class ErrorNotification(Error):
    '''
        Represents the errors related to notification related operations
        to the PagSeguro System.
    '''
    
    notification = models.ForeignKey(Notification, verbose_name=u'Notification')
     
    class Meta():
        verbose_name = u"Notification error"
        verbose_name_plural = u"Notification errors"
        
    def __unicode__(self):
        return "%d: %d - refering notification %s" % (self.id, self.code, self.notification.code)
    
    
class ErrorPayment(Error):
    '''
        Represents the errors related to Payment related operations
        to the PagSeguro System.
    '''
    
    payment = models.ForeignKey(Payment, verbose_name=u'Payment')
    
    class Meta():
        verbose_name = u"Payment error"
        verbose_name_plural = u"Payment errors"
        
    def __unicode__(self):
        return "%d: %d refering payment %s" % (self.id, self.code, self.payment.code)

