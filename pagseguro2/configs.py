#coding: utf-8

from django.conf import settings

PAGSEGURO_ENCODING = "ISO-8859-1"
PAGSEGURO_HTTPS_CONNECTION_HOST = "ws.pagseguro.uol.com.br"
PAGSEGURO_VERSION_PATH = "/v2/"
PAGSEGURO_REQUEST_CHECKOUT_SELECTOR_PREFIX = PAGSEGURO_VERSION_PATH + "checkout"
PAGSEGURO_REQUEST_NOTIFICATION_SELECTOR_PREFIX = PAGSEGURO_VERSION_PATH + "transactions/notifications/"
PAGSEGURO_REQUEST_TRANSACTION_SELECTOR_PREFIX = PAGSEGURO_VERSION_PATH + "transactions/"
PAGSEGURO_REQUEST_TYPE_POST = "POST"
PAGSEGURO_REQUEST_TYPE_GET = "GET"

PAGSEGURO_DEFAULT_HTTP_PARAMS = {'email':settings.PAGSEGURO_VENDOR_EMAIL,
                                 'token':settings.PAGSEGURO_VENDOR_TOKEN}

PAGSEGURO_CURRENCY = "BRL"

PAGSEGURO_HEADER_CONTENT_TYPE = "Content-Type"
PAGSEGURO_CONTENT_TYPE = "application/xml; Charset=%s" % (PAGSEGURO_ENCODING)
PAGSEGURO_HEADER_CONTENT_LENGTH = "Content-Length"

PAGSEGURO_REFERENCE_PREFIX = "VNREF"

PAGSEGURO_CLIENT_PAYMENT_HOST = "https://pagseguro.uol.com.br"
PAGSEGURO_CLIENT_PAYMENT_REDIRECT_URL = PAGSEGURO_CLIENT_PAYMENT_HOST + PAGSEGURO_REQUEST_CHECKOUT_SELECTOR_PREFIX + "/payment.html?%s"
                                        
PAGSEGURO_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


#===============================================================================
# Users of the django-pagseguro2 should declare the following configuration constants
# in the settings.py file of theirs projects:
#
# ==> PAGSEGURO_VENDOR_EMAIL: Email address registered with your pagseguro vendor account.
# ==> PAGSEGURO_VENDOR_TOKEN: PagSeguro automatically generated toked to identify your transactions.
# ==> PAGSEGURO_DEFAULT_REDIRECT_URL: A default redirect page for your payments (can be overwritten).
#===============================================================================
