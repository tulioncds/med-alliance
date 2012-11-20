#coding: utf-8

from django.contrib import admin
from models import Item, Payment, Transaction, Notification
from pagseguro2.models import ErrorPayment, ErrorNotification

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permition(self, request, obj=None):
        return False
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'amount')
    search_fields = ('__unicode__',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'created_on', 'answered_on', 'code', 'reference')
    search_fields = ('user','reference','code')
    list_filter = ('created_on', 'answered_on', 'method_type', 'method_code')
    ordering = ['-created_on']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'status', 'get_user')
    search_fields = ('reference',)
    list_filter = ('created_on', 'status', 'type')
    ordering = ['-created_on']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'received_on', 'checked')
    serch_fields = ('__unicode__',)
    list_filter = ('type', 'received_on', 'checked')
    
class ErrorNotificationAdmin(admin.ModelAdmin):
    pass

class ErrorPaymentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ErrorNotification, ErrorNotificationAdmin)
admin.site.register(ErrorPayment, ErrorPaymentAdmin)
