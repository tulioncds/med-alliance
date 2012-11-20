#coding: utf-8

from configs import *
from xml.dom import minidom
import httplib
import urllib
from pagseguro2 import UnauthorizedException

def post(selector=PAGSEGURO_VERSION_PATH, params=PAGSEGURO_DEFAULT_HTTP_PARAMS,
         content="", content_type=PAGSEGURO_CONTENT_TYPE):
    '''
        Sends a HTTP POST request to PagSeguro's API with given selector, 
        params, content and content_type.
        Commonly used in this module.
    '''
    
    query_char = '?' if '?' not in selector else '&'
    selector += query_char + urllib.urlencode(params)
     
    connection = httplib.HTTPSConnection(PAGSEGURO_HTTPS_CONNECTION_HOST)
    connection.connect()
    connection.putrequest(PAGSEGURO_REQUEST_TYPE_POST, selector)
    if content_type is not None:
        connection.putheader(PAGSEGURO_HEADER_CONTENT_TYPE, content_type)
    connection.putheader(PAGSEGURO_HEADER_CONTENT_LENGTH, str(len(content)))
    connection.endheaders()
    
    connection.send(content)
        
    return connection.getresponse().read()

def get(selector, params=PAGSEGURO_DEFAULT_HTTP_PARAMS):
    '''
        Sends a HTTP GET request to PagSeguro's API with given selector and params.
        Commonly used in this module.
    '''
    
    query_char = '?' if '?' not in selector else '&'
    selector += query_char + urllib.urlencode(params)
     
    connection = httplib.HTTPSConnection(PAGSEGURO_HTTPS_CONNECTION_HOST)
    connection.connect()
    connection.putrequest(PAGSEGURO_REQUEST_TYPE_GET, selector)
    connection.putheader(PAGSEGURO_HEADER_CONTENT_LENGTH, "0")
    connection.endheaders()
    
    connection.send("")
        
    return connection.getresponse().read()

def submit_payment(payment_document):
    '''
        Sends a the payment_document, a xml.dom.minidom.Document, 
        as submission to PagSeguro's API based on the congis.*
        Returns the correspondent xml.dom.minidom.Document of the response.
    '''
    
    response = post(PAGSEGURO_REQUEST_CHECKOUT_SELECTOR_PREFIX,
                    content=payment_document.toxml())
    try:
        # The xml.dom.minidom.Document version of the response
        return minidom.parseString(response)
    except:
        if response == UnauthorizedException.trigger:
            raise UnauthorizedException(payment_document.toprettyxml())
        
        

def check_notification(notification_code):
    '''
        Sends the notification_code in a notification query to PagSeguro's API 
        Returns the correspondent xml.dom.minidom.Document of the response.
    '''
    # The xml.dom.minidom.Document version of the response
    return minidom.parseString(get(PAGSEGURO_REQUEST_NOTIFICATION_SELECTOR_PREFIX \
                                   + notification_code))
    
def check_transaction(transaction_code):
    '''
        Sends the transaction_code in a transaction query to PagSeguro's API 
        Returns the correspondent xml.dom.minidom.Document of the response.
    '''
    # The xml.dom.minidom.Document version of the response
    return minidom.parseString(get(PAGSEGURO_REQUEST_TRANSACTION_SELECTOR_PREFIX \
                                   + transaction_code))
    
def query_transactions(initial_date, final_date, page=None,
                       max_page_results=None):
    '''
        Sends a period transaction query to PagSeguro's API 
        args:
            - intial_date, final_date: datetime.datetime
            - page: int
            - max_page_results: int
        Returns the correspondent xml.dom.minidom.Document of the response.
    '''

    params = PAGSEGURO_DEFAULT_HTTP_PARAMS.copy()
    
    params['initialDate'] = initial_date.strftime(PAGSEGURO_DATETIME_FORMAT)
    params['finalDate'] = final_date.strftime(PAGSEGURO_DATETIME_FORMAT)
    
    if page is not None:
        params['page'] = page
    if max_page_results is not None:
        params['maxPageResults'] = max_page_results
        
    # The xml.dom.minidom.Document version of the response
    return minidom.parseString(get(PAGSEGURO_REQUEST_TRANSACTION_SELECTOR_PREFIX,
                                   params))

