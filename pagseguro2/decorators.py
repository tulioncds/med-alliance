#coding: utf-8

from django.db import models
from models import Item

def payable(cls):
    '''
        This decorator makes the necessary changes to the decorated class cls
        in order to connect it to a pagseguro2.models.Item
    '''
    #======= This block inserts a pagseguro_item field into model class cls ====
    pagseguro_item = models.OneToOneField(Item, null=True, blank=True,
                                          verbose_name='pagseguro_item')
    #------- Meta data related to the field ------------------------------------
    pagseguro_item.opts = cls._meta
    pagseguro_item.name = 'pagseguro_item'
    pagseguro_item.column = '%s_id' % pagseguro_item.name 
    setattr(cls, pagseguro_item.name , pagseguro_item)
    cls._meta.add_field(pagseguro_item)
    #======= End of pagseguro_item insertion block =============================

    return cls
