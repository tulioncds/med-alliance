# -*- coding: utf-8 -*-
import re
from django import forms
from django.forms import ModelForm, Form, ValidationError, widgets
from django.contrib.localflavor.br import br_states, forms as br_forms
from models import Pessoa, Endereco, Telefone, Contato, Email, TIPO_ENDERECO
from widgets import *
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import smart_unicode
from django.forms.models import BaseInlineFormSet, inlineformset_factory,\
     modelform_factory, modelformset_factory
from django.forms.widgets import Media
from django.contrib.contenttypes.generic import generic_inlineformset_factory


phone_digits_re = re.compile(r'^(\d{2}) (\d{4})-(\d{4})$')
CHOICE_TIPO_ENDERECO = (('', '------'),) + TIPO_ENDERECO

class MyBRStateChoiceField(br_forms.BRStateChoiceField):
    default_error_messages = {
        'invalid': u'Estado inválido.',
    }
    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text=None):
        super(MyBRStateChoiceField, self).__init__(required, widget, label,
                                                 initial, help_text)
        self.widget.choices = (('', '------'),) + br_states.STATE_CHOICES

    def clean(self, value):
        value = super(MyBRStateChoiceField, self).clean(value)
        if value in EMPTY_VALUES and self.required:
            raise ValidationError(self.error_messages['required'])
        return value

class MyBRPhoneNumberField(br_forms.BRPhoneNumberField):
    default_error_messages = {'invalid': 'Ex: (XX) XXXX-XXXX'}

    def clean(self, value):
        super(MyBRPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\))', '', smart_unicode(value))
        m = phone_digits_re.search(value)
        if m:
            return u'(%s) %s-%s' % (m.group(1), m.group(2), m.group(3))
        raise ValidationError(self.error_messages['invalid'])

class EnderecoForm(ModelForm):
    class Meta:
        exclude= ('pessoa')

    logradouro = forms.CharField(required=False, label=u'Logradouro', help_text='(rua, avenida, logradouro, etc.)')
    numero  = forms.CharField(required=False, label=u'Número')
    cep = br_forms.BRZipCodeField(required=False,
                                  widget=Mask('99999-999'), label='CEP')
    uf = MyBRStateChoiceField(required=False, widget=forms.Select, label='UF')

    def __init__(self, *args,**kwargs):
        super(EnderecoForm,self).__init__(*args,**kwargs)
        self.fields['cep'].widget = Mask('99999-999')

class ContatoForm(ModelForm):
    class Meta:
        exclude= ('pessoa')

class EmailForm(ModelForm):
    class Meta:
        exclude= ('pessoa')

    email = forms.EmailField(label='Email')

class TelefoneForm(ModelForm):
    class Meta:
        exclude= ('pessoa')

    numero = MyBRPhoneNumberField(required=False,
                                  widget=Mask('(99) 9999-9999'),
                                  label=u'Número')
    ramal = forms.IntegerField(required=False,
                               widget=Mask('999999999'),
                               label='Ramal',)

EmailModelFormSet = modelformset_factory(Email, EmailForm, extra=1, can_delete=True)
EnderecoModelFormSet = modelformset_factory(Endereco, EnderecoForm, extra=1, can_delete=False)
ContatoModelFormSet = modelformset_factory(Contato, ContatoForm, extra=1, can_delete=True)
TelefoneModelFormSet = modelformset_factory(Telefone, TelefoneForm, extra=1, can_delete=True)

class PessoaForm(ModelForm):
    class Meta:
        exclude = ['created_at','updated_at', 'enderecos','telefones', 'emails', 'contatos']

    inlines = [EnderecoModelFormSet, TelefoneModelFormSet, EmailModelFormSet, ContatoModelFormSet]

    id = forms.IntegerField(required=False, widget=widgets.HiddenInput())
    cnpj = br_forms.BRCNPJField(required=False,
                                widget=MaskCNPJ(), label='CNPJ')
    cpf = br_forms.BRCPFField(required=False, widget=MaskCPF(), label='CPF')
    rg = forms.IntegerField(required=False,
                             widget=Mask('999999999999999999999999999'), label='RG')
    orgao_emissor = forms.CharField(required=False,
                                    label=u'Órgão Emissor',
                                    widget=Mask('aaaaaaaaaaaaaaa'))
    razao_social = forms.CharField(required=False,
                                    label=u'Razão Social')

    def __init__(self, *args,**kwargs):
        super(PessoaForm,self).__init__(*args,**kwargs)
        if self.fields.has_key('orgao_emissor'):
            self.fields['orgao_emissor'].widget = Mask('aaaaaaaaaaaaaaa')

    def _get_media(self):
       media = Media()
       for field in self.fields.values():
           media = media + field.widget.media
       for formset in self.inlines:
           media = media + formset(queryset=formset.model.objects.none()).media
       return media
    media = property(_get_media)

    def get_formsets(self, POST=None, obj_pessoa=None):
        formsets = []

        if POST:
            for index, formset in enumerate(self.inlines):
                if obj_pessoa:
                    formsets.append(formset(POST, queryset=formset.model.objects.filter(pessoa=obj_pessoa), prefix='fs%s'%index))
                else:
                    formsets.append(formset(POST, queryset=formset.model.objects.none(), prefix='fs%s'%index))
        else:
            for index, formset in enumerate(self.inlines):
                if obj_pessoa:
                    formsets.append(formset(queryset=formset.model.objects.filter(pessoa=obj_pessoa), prefix='fs%s'%index))
                else:
                    formsets.append(formset(queryset=formset.model.objects.none(), prefix='fs%s'%index))
        return formsets

    def save_formsets(self, formsets, obj_pessoa):
        for index, formset in enumerate(formsets):
            for object in formset.save():
                if index == 0:
                    obj_pessoa.enderecos.add(object)
                if index == 1:
                    obj_pessoa.telefones.add(object)
                if index == 2:
                    obj_pessoa.emails.add(object)
                if index == 3:
                    obj_pessoa.contatos.add(object)
        # return self.get_formsets(obj_pessoa=obj_pessoa)

    def valid_formsets(self, formsets):
        form_is_valid = True
        for formset in formsets:
            form_is_valid = form_is_valid and formset.is_valid()
        return form_is_valid
