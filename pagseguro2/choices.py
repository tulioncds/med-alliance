#coding: utf-8

STATUS_WAITING_FOR_PAYMENT = (1, 'Esperando Pagamento')
STATUS_UNDER_ANALISYS = (2, 'Em Análise')
STATUS_PAYED = (3, 'Pago')
STATUS_AVAILABLE = (4, 'Disponível')
STATUS_UNDER_DISPUTE = (5, 'Em Disputa')
STATUS_RETURNED = (6, 'Retornado')
STATUS_CANCELLED = (7, 'Cancelado')

STATUS_CHOICES = (STATUS_WAITING_FOR_PAYMENT,
                  STATUS_UNDER_ANALISYS,
                  STATUS_PAYED,
                  STATUS_AVAILABLE,
                  STATUS_UNDER_DISPUTE,
                  STATUS_RETURNED,
                  STATUS_CANCELLED)

# Payment method types and its 'choices' creation

PAYMENT_METHOD_TYPE_CREDIT_CARD = (1, 'Cartão de Crédito')
PAYMENT_METHOD_TYPE_BILLET = (2, 'Boleto')
PAYMENT_METHOD_TYPE_ONLINE_DEBIT = (3, 'Débito Online')
PAYMENT_METHOD_TYPE_PAGSEGURO_BALANCE = (4, 'PagSeguro Balance')
PAYMENT_METHOD_TYPE_OIPAGGO = (5, 'Oi Paggo')

PAYMENT_METHOD_TYPE_CHOICES = (PAYMENT_METHOD_TYPE_CREDIT_CARD,
                               PAYMENT_METHOD_TYPE_BILLET,
                               PAYMENT_METHOD_TYPE_ONLINE_DEBIT,
                               PAYMENT_METHOD_TYPE_PAGSEGURO_BALANCE,
                               PAYMENT_METHOD_TYPE_OIPAGGO)
    
    

# Payment method codes and its 'choices' creation

PAYMENT_METHOD_CODE_VISA_CREDIT_CARD = (101, 'Visa')
PAYMENT_METHOD_CODE_MASTERCARD_CREDIT_CARD = (102, 'MasterCard')
PAYMENT_METHOD_CODE_AMEX_CREDIT_CARD = (103, 'American Express')
PAYMENT_METHOD_CODE_DINERS_CREDIT_CARD = (104, 'Diners')
PAYMENT_METHOD_CODE_HIPERCARD_CREDIT_CARD = (105, 'Hipercard')
PAYMENT_METHOD_CODE_AURA_CREDIT_CARD = (106, 'Aura')
PAYMENT_METHOD_CODE_ELO_CREDIT_CARD = (107, 'Elo')
PAYMENT_METHOD_CODE_BILLET_BRADESCO = (201, 'Bradesco Boleto')
PAYMENT_METHOD_CODE_BILLET_SANTANDER = (202, 'Santander Boleto')
PAYMENT_METHOD_CODE_BRADESCO_ONLINE_DEBIT = (301, 'Bradesco Débito online')
PAYMENT_METHOD_CODE_ITAU_ONLINE_DEBIT = (302, 'Itau Débito online')
PAYMENT_METHOD_CODE_UNIBANCO_ONLINE_DEBIT = (303, 'Unibanco Débito online')
PAYMENT_METHOD_CODE_BANCODOBRASIL_ONLINE_DEBIT = (304, 'Banco do Brasil Débito online')
PAYMENT_METHOD_CODE_BANCOREAL_ONLINE_DEBIT = (305, 'Banco Real Débito online')
PAYMENT_METHOD_CODE_BANRISUL_ONLINE_DEBIT = (306, 'Banrisul Débito online')
PAYMENT_METHOD_CODE_HSBC_ONLINE_DEBIT = (307, 'HSBC Débito online')
PAYMENT_METHOD_CODE_PAGSEGURO_BALANCE = (401, 'PagSeguro Balance')
PAYMENT_METHOD_CODE_OIPAGGO = (501, 'Oi Paggo')

PAYMENT_METHOD_CODE_CHOICES = (PAYMENT_METHOD_CODE_VISA_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_MASTERCARD_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_AMEX_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_DINERS_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_HIPERCARD_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_AURA_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_ELO_CREDIT_CARD,
                               PAYMENT_METHOD_CODE_BILLET_BRADESCO,
                               PAYMENT_METHOD_CODE_BILLET_SANTANDER,
                               PAYMENT_METHOD_CODE_BRADESCO_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_ITAU_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_UNIBANCO_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_BANCODOBRASIL_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_BANCOREAL_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_BANRISUL_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_HSBC_ONLINE_DEBIT,
                               PAYMENT_METHOD_CODE_PAGSEGURO_BALANCE,
                               PAYMENT_METHOD_CODE_OIPAGGO)



# Type transactions and its 'choices' creation
 
TYPE_TRANSACTION = (1, 'Transaction')

TYPE_CHOICES = (TYPE_TRANSACTION,)



# Notification check status and its 'choices' creation

CHECKED_NO = (1, "Not checked")
CHECKED_YES_SUCCESS = (2, "Checked with success")
CHECKED_YES_FAILURE = (3, "Checked with failure")

CHECKED_CHOICES = (CHECKED_NO,
                   CHECKED_YES_SUCCESS,
                   CHECKED_YES_FAILURE)
    
    
    
# Payment status and its 'choices' creation

EMAIL_IS_REQUIRED = (10001, u"Email is required.")
TOKEN_IS_REQUIRED = (10002, u"Token is required.")
EMAIL_INVALID_VALUE = (10003, u"Email invalid value.")
RECEIVEREMAIL_IS_REQUIRED = (11001, u"receiverEmail is required.")
RECEIVEREMAIL_INVALID_LENGTH = (11002, u"receiverEmail invalid length: {0}")
RECEIVEREMAIL_INVALID_VALUE = (11003, u"receiverEmail invalid value.")
CURRENCY_IS_REQUIRED = (11004, u"Currency is required.")
CURRENCY_INVALID_VALUE = (11005, u"Currency invalid value: {0}")
REDIRECTURL_INVALID_LENGTH = (11006, u"redirectURL invalid length: {0}")
REDIRECTURL_INVALID_VALUE = (11007, u"redirectURL invalid value: {0}")
REFERENCE_INVALID_LENGTH = (11008, u"reference invalid length: {0}")
SENDEREMAIL_INVALID_LENGTH = (11009, u"senderEmail invalid length: {0}")
SENDEREMAIL_INVALID_VALUE = (11010, u"senderEmail invalid value: {0}")
SENDERNAME_INVALID_LENGTH = (11011, u"senderName invalid length: {0}")
SENDERNAME_INVALID_VALUE = (11012, u"senderName invalid value: {0}")
SENDERAREACODE_INVALID_VALUE = (11013, u"senderAreaCode invalid value: {0}")
SENDERPHONE_INVALID_VALUE = (11014, u"senderPhone invalid value: {0}")
SHIPPINGTYPE_IS_REQUIRED = (11015, u"ShippingType is required.")
SHIPPINGTYPE_INVALID_TYPE = (11016, u"shippingType invalid type: {0}")
SHIPPINGPOSTALCODE_INVALID_VALUE = (11017, u"shippingPostalCode invalid Value: {0}")
SHIPPINGADDRESSSTREET_INVALID_LENGTH = (11018, u"shippingAddressStreet invalid length: {0}")
SHIPPINGADDRESSNUMBER_INVALID_LENGTH = (11019, u"shippingAddressNumber invalid length: {0}")
SHIPPINGADDRESSCOMPLEMENT_INVALID_LENGTH = (11020, u"shippingAddressComplement invalid length: {0}")
SHIPPINGADDRESSDISTRICT_INVALID_LENGTH = (11021, u"shippingAddressDistrict invalid length: {0}")
SHIPPINGADDRESSCITY_INVALID_LENGTH = (11022, u"shippingAddressCity invalid length: {0}")
SHIPPINGADDRESSSTATE_INVALID_VALUE = (11023, u"shippingAddressState invalid value: {0}, must fit the pattern: \w\{2\} (e. g. 'SP')")
ITENS_INVALID_QUANTITY = (11024, u"Itens invalid quantity.")
ITEM_ID_IS_REQUIRED = (11025, u"Item Id is required.")
ITEM_QUANTITY_IS_REQUIRED = (11026, u"Item quantity is required.")
ITEM_QUANTITY_OUT_OF_RANGE = (11027, u"Item quantity out of range: {0}")
ITEM_AMOUNT_IS_REQUIRED = (11028, u"Item amount is required. (e.g. '12.00')")
ITEM_AMOUNT_INVALID_PATTERN = (11029, u"Item amount invalid pattern: {0}. Must fit the patern: \d+.\d\{2\}")
ITEM_AMOUNT_OUT_OF_RANGE = (11030, u"Item amount out of range: {0}")
ITEM_SHIPPINGCOST_INVALID_PATTERN = (11031, u"Item shippingCost invalid pattern: {0}. Must fit the patern: \d+.\d\{2\}")
ITEM_SHIPPINGCOST_OUT_OF_RANGE = (11032, u"Item shippingCost out of range: {0}")
ITEM_DESCRIPTION_IS_REQUIRED = (11033, u"Item description is required.")
ITEM_DESCRIPTION_INVALID_LENGTH = (11034, u"Item description invalid length: {0}")
ITEM_WEIGHT_INVALID_VALUE = (11035, u"Item weight invalid Value: {0}")
EXTRA_AMOUNT_INVALID_PATTERN = (11036, u"Extra amount invalid pattern: {0}. Must fit the patern: -?\d+.\d\{2\}")
EXTRA_AMOUNT_OUT_OF_RANGE = (11037, u"Extra amount out of range: {0}")
INVALID_RECEIVER_FOR_CHECKOUT = (11038, u"Invalid receiver for checkout: {0}, verify receiver's account status.")
MALFORMED_REQUEST_XML = (11039, u"Malformed request XML: {0}.")
MAXAGE_INVALID_PATTERN = (11040, u"maxAge invalid pattern: {0}. Must fit the patern: \d+")
MAXAGE_OUT_OF_RANGE = (11041, u"maxAge out of range: {0}")
MAXUSES_INVALID_PATTERN = (11042, u"maxUses invalid pattern: {0}. Must fit the patern: \d+")
MAXUSES_OUT_OF_RANGE = (11043, u"maxUses out of range.")
INITIALDATE_IS_REQUIRED = (11044, u"initialDate is required.")
INITIALDATE_MUST_BE_LOWER_THAN_ALLOWED_LIMIT = (11045, u"initialDate must be lower than allowed limit.")
INITIALDATE_MUST_NOT_BE_OLDER_THAN_6_MONTHS = (11046, u"initialDate must not be older than 6 months.")
INITIALDATE_MUST_BE_LOWER_THAN_OR_EQUAL_FINALDATE = (11047, u"initialDate must be lower than or equal finalDate.")
SEARCH_INTERVAL_MUST_BE_LOWER_THAN_OR_EQUAL_30_DAYS = (11048, u"search interval must be lower than or equal 30 days.")
FINALDATE_MUST_BE_LOWER_THAN_ALLOWED_LIMIT = (11049, u"finalDate must be lower than allowed limit.")
INITIALDATE_INVALID_FORMAT = (11050, u"initialDate invalid format, use 'yyyy-MM-ddTHH:mm' (eg. 2010-01-27T17:25).")
FINALDATE_INVALID_FORMAT = (11051, u"finalDate invalid format, use 'yyyy-MM-ddTHH:mm' (eg. 2010-01-27T17:25).")
PAGE_INVALID_VALUE = (11052, u"page invalid value.")
MAXPAGERESULTS_INVALID_VALUE = (11053, u"maxPageResults invalid value (must be between 1 and 1000).")
ABANDONURL_INVALID_LENGTH = (11054, u"abandonURL invalid length: {0}")
ABANDONURL_INVALID_VALUE = (11055, u"abandonURL invalid value: {0}")
SENDER_ADDRESS_REQUIRED_INVALID_VALUE = (11056, u"sender address required invalid value: {0}")
SENDER_ADDRESS_NOT_REQUIRED_WITH_ADDRESS_DATA_FILLED = (11057, u"sender address not required with address data filled")

ERROR_CHOICES = (EMAIL_IS_REQUIRED,
                  TOKEN_IS_REQUIRED,
                  EMAIL_INVALID_VALUE,
                  RECEIVEREMAIL_IS_REQUIRED,
                  RECEIVEREMAIL_INVALID_LENGTH,
                  RECEIVEREMAIL_INVALID_VALUE,
                  CURRENCY_IS_REQUIRED,
                  CURRENCY_INVALID_VALUE,
                  REDIRECTURL_INVALID_LENGTH,
                  REDIRECTURL_INVALID_VALUE,
                  REFERENCE_INVALID_LENGTH,
                  SENDEREMAIL_INVALID_LENGTH,
                  SENDEREMAIL_INVALID_VALUE,
                  SENDERNAME_INVALID_LENGTH,
                  SENDERNAME_INVALID_VALUE,
                  SENDERAREACODE_INVALID_VALUE,
                  SENDERPHONE_INVALID_VALUE,
                  SHIPPINGTYPE_IS_REQUIRED,
                  SHIPPINGTYPE_INVALID_TYPE,
                  SHIPPINGPOSTALCODE_INVALID_VALUE,
                  SHIPPINGADDRESSSTREET_INVALID_LENGTH,
                  SHIPPINGADDRESSNUMBER_INVALID_LENGTH,
                  SHIPPINGADDRESSCOMPLEMENT_INVALID_LENGTH,
                  SHIPPINGADDRESSDISTRICT_INVALID_LENGTH,
                  SHIPPINGADDRESSCITY_INVALID_LENGTH,
                  SHIPPINGADDRESSSTATE_INVALID_VALUE,
                  ITENS_INVALID_QUANTITY,
                  ITEM_ID_IS_REQUIRED,
                  ITEM_QUANTITY_IS_REQUIRED,
                  ITEM_QUANTITY_OUT_OF_RANGE,
                  ITEM_AMOUNT_IS_REQUIRED,
                  ITEM_AMOUNT_INVALID_PATTERN,
                  ITEM_AMOUNT_OUT_OF_RANGE,
                  ITEM_SHIPPINGCOST_INVALID_PATTERN,
                  ITEM_SHIPPINGCOST_OUT_OF_RANGE,
                  ITEM_DESCRIPTION_IS_REQUIRED,
                  ITEM_DESCRIPTION_INVALID_LENGTH,
                  ITEM_WEIGHT_INVALID_VALUE,
                  EXTRA_AMOUNT_INVALID_PATTERN,
                  EXTRA_AMOUNT_OUT_OF_RANGE,
                  INVALID_RECEIVER_FOR_CHECKOUT,
                  MALFORMED_REQUEST_XML,
                  MAXAGE_INVALID_PATTERN,
                  MAXAGE_OUT_OF_RANGE,
                  MAXUSES_INVALID_PATTERN,
                  MAXUSES_OUT_OF_RANGE,
                  INITIALDATE_IS_REQUIRED,
                  INITIALDATE_MUST_BE_LOWER_THAN_ALLOWED_LIMIT,
                  INITIALDATE_MUST_NOT_BE_OLDER_THAN_6_MONTHS,
                  INITIALDATE_MUST_BE_LOWER_THAN_OR_EQUAL_FINALDATE,
                  SEARCH_INTERVAL_MUST_BE_LOWER_THAN_OR_EQUAL_30_DAYS,
                  FINALDATE_MUST_BE_LOWER_THAN_ALLOWED_LIMIT,
                  INITIALDATE_INVALID_FORMAT,
                  FINALDATE_INVALID_FORMAT,
                  PAGE_INVALID_VALUE,
                  MAXPAGERESULTS_INVALID_VALUE,
                  ABANDONURL_INVALID_LENGTH,
                  ABANDONURL_INVALID_VALUE,
                  SENDER_ADDRESS_REQUIRED_INVALID_VALUE,
                  SENDER_ADDRESS_NOT_REQUIRED_WITH_ADDRESS_DATA_FILLED,)

