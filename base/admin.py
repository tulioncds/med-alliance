# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from forms import *

class EnderecoAdmin(admin.ModelAdmin):
    form = EnderecoForm

class EnderecoInline(admin.TabularInline):
    verbose_name = u'Endereço'
    verbose_name_plural = u'Endereços'
    extra = 1

class TelefoneAdmin(admin.ModelAdmin):
    form = TelefoneForm

class TelefoneInline(admin.TabularInline):
    verbose_name = u'Telefone'
    verbose_name_plural = u'Telefones'
    extra = 1

class EmailAdmin(admin.ModelAdmin):
    form = EmailForm

class EmailInline(admin.TabularInline):
    verbose_name = u'Email'
    verbose_name_plural = u'Emails'
    extra = 1

class ContatoAdmin(admin.ModelAdmin):
    form = ContatoForm

class ContatoInline(admin.TabularInline):
    verbose_name = u'Contato'
    verbose_name_plural = u'Contatos'
    extra = 1
