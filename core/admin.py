# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from models import Paciente, Medico, Clinica, Holiday, EventoMedico,\
                   Pergunta, Resposta, Consulta

from base.admin import *

from schedule.models import Event, Calendar

class PacienteEnderecoInline(EnderecoInline):
    model = Paciente.enderecos.through

class MedicoEnderecoInline(EnderecoInline):
    model = Medico.enderecos.through

class ClinicaEnderecoInline(EnderecoInline):
    model = Clinica.enderecos.through

class PacienteTelefoneInline(TelefoneInline):
    model = Paciente.telefones.through

class MedicoTelefoneInline(TelefoneInline):
    model = Medico.telefones.through

class ClinicaTelefoneInline(TelefoneInline):
    model = Clinica.telefones.through

class PacienteEmailInline(EmailInline):
    model = Paciente.emails.through

class MedicoEmailInline(EmailInline):
    model = Medico.emails.through

class ClinicaEmailInline(EmailInline):
    model = Clinica.emails.through

class PacienteContatoInline(ContatoInline):
    model = Paciente.contatos.through

class MedicoContatoInline(ContatoInline):
    model = Medico.contatos.through

class ClinicaContatoInline(ContatoInline):
    model = Clinica.contatos.through

class PacienteForm(PessoaForm):

    class Meta(PessoaForm.Meta):
        model = Paciente
        exclude = ['cnpj', 'razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'id']

class PacienteAdmin(admin.ModelAdmin):
    form = PacienteForm
    inlines = [PacienteEnderecoInline, PacienteTelefoneInline, PacienteEmailInline, PacienteContatoInline,]
    search_fields = ['nome',]
    actions = ['enviar_emails',]

    def enviar_emails(self, request, queryset):
        url = reverse('admin_email_pacientes')
        ids = []
        for paciente in queryset:
            ids.append(str(paciente.pk))
        if len(ids) > 0:
            url+='?ids=' + ','.join(ids)
        return HttpResponseRedirect(url)
    enviar_emails.short_description = "Enviar email para os Pacientes"

class MedicoForm(PessoaForm):

    class Meta(PessoaForm.Meta):
        model = Medico
        exclude = ['cnpj', 'razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'id']

class MedicoAdmin(admin.ModelAdmin):
    form = MedicoForm
    search_fields = ['nome', 'bairro', 'estado', 'municipio']
    list_filter = (
            'clinica',
            'municipio',
    )
    list_display = ('nome', 'crm', 'get_especialidade', 'estado', 'municipio', 'bairro')
    inlines = [MedicoEnderecoInline, MedicoTelefoneInline, MedicoEmailInline, MedicoContatoInline,]

class ClinicaForm(PessoaForm):

    class Meta:
        model = Clinica
        exclude = ['enderecos', 'telefones', 'emails', 'contatos', 'rg', 'cpf', 'id', 'orgao_emissor',]

class ClinicaAdmin(admin.ModelAdmin):
    form = ClinicaForm
    search_fields = ['nome', 'bairro', 'estado', 'municipio']
    list_filter = (
            'municipio',
    )
    list_display = ('nome', 'estado', 'municipio', 'bairro')
    inlines = [ClinicaEnderecoInline, ClinicaTelefoneInline, ClinicaEmailInline, ClinicaContatoInline,]

class HolidayAdmin(admin.ModelAdmin):
    model = Holiday

class RespostaAdmin(admin.ModelAdmin):
    model = Resposta
    search_fields = ['conteudo', 'paciente', 'medico',]
    list_display = (
            'medico',
            'paciente',
            'conteudo',
            'data_hora',
    )
    list_filter = (
            'medico',
            'paciente',
            'data_hora',
    )

class PerguntaAdmin(admin.ModelAdmin):
    model = Pergunta
    search_fields = ['conteudo', 'paciente', 'medico',]
    list_display = (
            'medico',
            'paciente',
            'conteudo',
            'data_hora',
            'lida',
    )
    list_filter = (
            'medico',
            'paciente',
            'data_hora',
            'lida',
    )

class EventoMedicoAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=True)
        for medico in instance.medicos.all():
            calendario = Calendar.objects.get_or_create_calendar_for_object(
                medico,
                name='Dr. %s' % medico.nome,
            )
            Event.objects.create(
                start=instance.inicio,
                end=instance.fim,
                title=instance.titulo,
                description=instance.descricao,
                creator=request.user,
                calendar=calendario,
            )
            message = render_to_string(
                'core/novo_evento.txt', 
                {'medico': medico, 'evento': instance}
            )
        emails = map(lambda x: x.user.email, instance.medicos.all())
        send_mail(instance.titulo, message, settings.EMAIL_HOST_USER, emails)
        return instance

class ConsultaAdmin(admin.ModelAdmin):
    model = Consulta
    list_filter = (
            'medico',
            'paciente',
            'start',
            'end',
    )
    list_display = (
            'start',
            'end',
            'medico',
            'paciente'
    )

admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Telefone, TelefoneAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Contato, ContatoAdmin)
admin.site.register(Clinica, ClinicaAdmin)
admin.site.register(Holiday, HolidayAdmin)
admin.site.register(EventoMedico, EventoMedicoAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(Consulta, ConsultaAdmin)
