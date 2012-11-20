from django.conf import settings

class UnauthorizedException(Exception):
    trigger = "Unauthorized"
    msg = "Your payment submition was not accepted by the PagSeguro System.\n" +\
               "This has probably been caused by a misconfiguration problem in your settings.py file.\n" +\
               "Here is some data you should check for correctness.\n\n" +\
               "PAGSEGURO_VENDOR_TOKEN = %s\n" +\
               "PAGSEGURO_VENDOR_EMAIL = %s\n" +\
               "Submited payment XML file:\n%s" 

    def __init__(self, xml):
        self.xml = xml
    
    def __str__(self):
        return self.msg %(settings.PAGSEGURO_VENDOR_TOKEN, settings.PAGSEGURO_VENDOR_EMAIL, self.xml)
         