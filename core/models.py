# -*- coding: utf-8 -*-
from django.db import models
from base.models import Pessoa
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from registration import signals

from base.models import Email
from schedule.models.events import Event
from pagseguro2.models import Item, Payment

class UserProfile(models.Model):
    USER_TYPES = (
            ('P', 'Paciente'),
            ('M', u'Médico'),
            ('C', u'Clínica'),
    )

    user = models.OneToOneField(User, related_name='profile')
    tipo_usuario = models.CharField(max_length=1, choices=USER_TYPES)

def create_user_profile(sender, user, request, **kwargs):

    if user:
        if 'dados' in kwargs:

            tipo_usuario = kwargs['dados']['tipo_usuario']

            if tipo_usuario == 'P':
                nome, cpf, rg, orgao_emissor = kwargs['dados']['nome'],\
                                               kwargs['dados']['cpf'],\
                                               kwargs['dados']['rg'],\
                                               kwargs['dados']['orgao_emissor']

                Paciente.objects.create(nome=nome, cpf=cpf, rg=rg, orgao_emissor=orgao_emissor, user=user, tipo_usuario=tipo_usuario)

            elif tipo_usuario == 'M':
                nome, cpf, rg, orgao_emissor, crm, especialidade, clinica = kwargs['dados']['nome'],\
                                                                            kwargs['dados']['cpf'],\
                                                                            kwargs['dados']['rg'],\
                                                                            kwargs['dados']['orgao_emissor'],\
                                                                            kwargs['dados']['crm'],\
                                                                            kwargs['dados']['especialidade'],\
                                                                            kwargs['dados']['clinica']

                Medico.objects.create(nome=nome, cpf=cpf, rg=rg, orgao_emissor=orgao_emissor, user=user, crm=crm, especialidade=especialidade, clinica=clinica, tipo_usuario=tipo_usuario)

            elif tipo_usuario == 'C':
                nome, cnpj, razao_social, = kwargs['dados']['nome'],\
                                            kwargs['dados']['cnpj'],\
                                            kwargs['dados']['razao_social']

                Clinica.objects.create(nome=nome, cnpj=cnpj, razao_social=razao_social, user=user, tipo_usuario=tipo_usuario)

        else:
            UserProfile.objects.create(user=user)
signals.user_registered.connect(create_user_profile)

class Holiday(models.Model):
    date = models.DateField()

    def __unicode__(self):
        return unicode(self.date)

class Paciente(Pessoa, UserProfile):

    class Meta:
        verbose_name_plural = u'Pacientes'

    def __unicode__(self):
        return self.nome or ''


class Clinica(Pessoa, UserProfile):

    class Meta:
        verbose_name = u'Clínica'
        verbose_name_plural = u'Clínicas'

    bairro = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.nome or ''


class Medico(Pessoa, UserProfile):

    ESPECIALIDADES = (
            ('CARDIO', 'Cardiologista'),
            ('NEURO', 'Neurologista'),
            ('NEFRO', 'Nefrologista'),
            ('ANEST', 'Anestesista'),
            ('PNEUMO', 'Pneumologista'),
            ('ANCO', 'Ancologista'),
            ('GINECO', 'Ginecologista'),
            ('OTORRINO', 'Otorrinolaringologista'),
            ('PATO', 'Patologista'),
    )

    class Meta:
        verbose_name = u'Médico'
        verbose_name_plural = u'Médicos'

    crm = models.CharField(max_length=5, verbose_name="CRM")
    especialidade = models.CharField(max_length=50, choices=ESPECIALIDADES)
    clinica = models.ForeignKey(Clinica, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    municipio = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True)

    def __unicode__(self):
        return self.nome or ''

    @classmethod
    def get_especialidades(cls):
        return cls.ESPECIALIDADES

    def get_especialidade(self):
        return self.get_especialidade_display()
    get_especialidade.short_description = 'Especialidade'

class Consulta(Event):

    def __unicode__(self):
        return 'Consulta {0}'.format(self.pk)

    medico = models.ForeignKey(Medico)
    paciente = models.ForeignKey(Paciente)
    pagamento = models.ForeignKey(Payment, null=True, blank=True)
    paga = models.BooleanField(default=False)

class EventoMedico(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(null=True, blank=True)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    medicos = models.ManyToManyField(Medico)

class Pergunta(models.Model):

    def __unicode__(self):
        return self.conteudo[:75] + (self.conteudo[75:] and '...') or ''

    medico = models.ForeignKey(Medico)
    paciente = models.ForeignKey(Paciente)
    conteudo = models.TextField(verbose_name=u'Conteúdo')
    lida = models.BooleanField(verbose_name='Respondida')
    data_hora = models.DateTimeField()

class Resposta(models.Model):

    def __unicode__(self):
        return self.conteudo[:75] + (self.conteudo[75:] and '...') or ''

    medico = models.ForeignKey(Medico)
    pergunta = models.ForeignKey(Pergunta)
    paciente = models.ForeignKey(Paciente)
    conteudo = models.TextField()
    data_hora = models.DateTimeField()
