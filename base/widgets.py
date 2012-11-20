# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.template.loader import render_to_string

class Mask(forms.TextInput):
    """
    Widget que acrescenta qualquer a mascara recebido no construtor
    """
    class Media:
        js = (settings.STATIC_URL + "jquery/js/jquery.metadata.js",
              settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/maskwidget.js",)

    def __init__(self, mask, attrs={}):
        new_attrs = attrs

        if not re.match(r'\{.*\}', mask):
            mask = "{mask: '%s'}" % mask

#        if 'class' in attrs and mask not in attrs['class']:
#            new_attrs = {'class': ' %s %s ' % (attrs['class'], mask)}
#        else:
        new_attrs['class'] = mask 
        super(Mask, self).__init__(
            attrs=new_attrs
        )


class MaskDate(forms.DateInput):
    """
    Widget que coloca o datepicker do jqueryui no input. Além disso acrescenta
    a mascara de data, para forcar a digitacao no padrao esperado.
    """
    class Media:
        js = (settings.STATIC_URL + "jqueryui/js/jquery.ui.datepicker.js",
              settings.STATIC_URL + "jqueryui/js/jquery.ui.datepicker-pt-BR.js",
              settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/datewidget.js",)

    def __init__(self, attrs={}):
        new_attrs = {'class': ' datePicker ', 'size': '10', 'alt': 'date'}
        new_attrs.update(attrs)
        super(MaskDate, self).__init__(
            attrs=new_attrs,
            format='%d/%m/%Y'
        )

class MaskCurrency(forms.TextInput):
    """
    Widget que acrescenta a mascara de valor decimal, para forcar a digitacao
    no padrao esperado. 
    """
    class Media:
        js = (settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/maskwidget.js",)

    def __init__(self, attrs={}):
        attrs['alt'] = 'decimal'
        super(MaskCurrency, self).__init__(
            attrs=attrs
        )

class MaskInteger(forms.TextInput):
    """
    Widget que acrescenta a mascara de inteiro, para forcar a digitacao
    de apenas inteiros. 
    """
    class Media:
        js = (settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/maskwidget.js",)

    def __init__(self, attrs={}):
        attrs['alt'] = 'integer'
        super(MaskInteger, self).__init__(
            attrs=attrs
        )

class MaskCNPJ(forms.TextInput):
    """
    Widget que acrescenta a mascara de CNPJ, para forcar a digitacao
    de apenas inteiros no padrao que se espera.
    """
    class Media:
        js = (settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/maskwidget.js",)

    def __init__(self, attrs={}):
        attrs['alt'] = 'cnpj'
        super(MaskCNPJ, self).__init__(
            attrs=attrs
        )

class MaskCPF(forms.TextInput):
    """
    Widget que acrescenta a mascara de CPF, para forcar a digitacao
    de apenas inteiros no padrao que se espera. 
    """
    class Media:
        js = (settings.STATIC_URL + "jquery/js/jquery.meio.mask.min.js",
              settings.STATIC_URL + "site/js/maskwidget.js",)

    def __init__(self, attrs={}):
        attrs['alt'] = 'cpf'
        super(MaskCPF, self).__init__(
            attrs=attrs
        )

