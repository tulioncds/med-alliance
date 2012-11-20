# -*- coding: utf-8 -*-
from django.db import models
from geocode import GeoCodeField
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^geocode\.GeoCodeField"])

ENDERECO_RESIDENCIAL = 'ERE'
ENDERECO_COMERCIAL = 'ECO'
ENDERECO_OUTRO = 'TOU'
TIPO_ENDERECO = (
                  (ENDERECO_RESIDENCIAL, u'Residencial'),
                  (ENDERECO_COMERCIAL, u'Comercial'),
                  (ENDERECO_OUTRO, u'Outro'),
                  )

class Endereco(models.Model):
    class Meta:
        verbose_name = u'Endereço'
        verbose_name_plural = u'Endereços'

    tipo = models.CharField(max_length=255, null=True, blank=True,
                            choices=TIPO_ENDERECO, editable=False)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=255,
                              null=True, blank=True)
    complemento = models.CharField(max_length=255,
                                   null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    uf = models.CharField(max_length=255, null=True, blank=True)
    geocode = GeoCodeField(null=True, blank=True, max_length=255, editable=False)

    #usado pelo GeoCodeField
    def get_geocode_info(self):
        """ metodo necessario pelo  GeoCodeField """
        endereco = ' '.join([
                self.logradouro or '',
                self.numero or '',
                self.bairro or '',
                self.cidade or '',
                self.uf or ''
        ])
        return u'Endereço', endereco

    #usado pelo GeoCodeField
    def set_address(self, address):
        """ metodo necessario pelo  GeoCodeField """
        self.endereco = address

    def get_endereco_completo(self):
        completo = []
        if self.logradouro:
            completo.append(self.logradouro)
        if self.numero:
            completo.append(self.numero)
        if self.complemento:
            completo.append(self.complemento)
        if self.bairro:
            completo.append(self.bairro)
        if self.cidade:
            if self.uf:
                completo.append(self.cidade + '-' + self.uf)
            else:
                completo.append(self.cidade)
        if self.uf and not self.cidade:
            completo.append(self.uf)
        resposta = ', '.join(completo)
        if self.tipo:
            resposta += " (" + self.get_tipo_display() + ")"
        return resposta

    def __unicode__(self):
        return unicode(self.get_endereco_completo())

class Contato(models.Model):
    class Meta:
        verbose_name = u'Contato'
        verbose_name_plural = u'Contatos'

    msn = models.EmailField(null=True, blank=True)
    twitter = models.URLField(verify_exists=False, max_length=255, default='',
                           null=True, blank=True)
    site = models.URLField(verify_exists=False, max_length=255, default='',
                           null=True, blank=True)
    blog = models.URLField(verify_exists=False, max_length=255, default='',
                           null=True, blank=True)
    facebook = models.URLField(verify_exists=False, max_length=255, default='',
                           null=True, blank=True)
    orkut = models.URLField(verify_exists=False, max_length=255, default='',
                           null=True, blank=True)

    def get_contato(self):
        contatos = [item for item in [self.msn, self.twitter, self.site, self.blog, self.facebook, self.orkut] if item]
        contato = ', '.join(contatos)
        return contato

    def __unicode__(self):
        return unicode(self.get_contato())

class Email(models.Model):
    class Meta:
        verbose_name = u'E-mail'
        verbose_name_plural = u'E-mails'

    email = models.EmailField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.email)

TEL_RESIDENCIAL = 'TRE'
TEL_COMERCIAL = 'TCO'
TEL_CELULAR = 'CEL'
TEL_OUTRO = 'TOU'
TIPO_TELEFONE = (
                  (TEL_RESIDENCIAL, 'Residencial'),
                  (TEL_COMERCIAL, 'Comercial'),
                  (TEL_CELULAR, 'Celular'),
                  (TEL_OUTRO, 'Outro'),
                  )


class Telefone(models.Model):
    class Meta:
        verbose_name = u'Telefone'
        verbose_name_plural = u'Telefones'

    tipo = models.CharField(max_length=255, null=True, blank=True,
                            choices=TIPO_TELEFONE)
    numero = models.CharField(max_length=14, default='',
                                              null=True, blank=True)
    ramal = models.CharField(max_length=14, default='',
                                              null=True, blank=True)

    def __unicode__(self):
        return unicode(self.numero)

class Pessoa(models.Model):
    class Meta:
        verbose_name = u'Pessoa'
        verbose_name_plural = u'Pessoas'
        abstract = True

    pessoa_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nome = models.CharField(max_length=255, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    rg = models.CharField(max_length=30, null=True, blank=True)
    orgao_emissor = models.CharField(max_length=30, null=True, blank=True)
    cnpj = models.CharField(max_length=18, null=True, blank=True)
    razao_social = models.CharField(max_length=255, null=True, blank=True)
    enderecos = models.ManyToManyField(Endereco, related_name="%(app_label)s_%(class)s_related")
    telefones = models.ManyToManyField(Telefone, related_name="%(app_label)s_%(class)s_related")
    emails = models.ManyToManyField(Email, related_name="%(app_label)s_%(class)s_related")
    contatos = models.ManyToManyField(Contato, related_name="%(app_label)s_%(class)s_related")

    def __unicode__(self):
        return unicode(self.nome)
