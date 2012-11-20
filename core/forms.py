# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from base.forms import PessoaForm, EnderecoForm
from models import Paciente, Medico, Clinica
from django.forms.models import modelformset_factory
from base.models import Endereco

class AdminEmailPacientesForm(forms.Form):

    titulo = forms.CharField(label=u'Título', required=True)
    conteudo = forms.CharField(widget=forms.Textarea, label=u'Conteúdo', required=True)

class PacienteForm(PessoaForm):
    class Meta:
        model = Paciente
        exclude = ('razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'cnpj', 'user')

    username = forms.CharField(label=u'Nome de usuário')
    email = forms.EmailField()
    password1 = forms.CharField(label=u'Senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirme a senha', widget=forms.PasswordInput())
    tipo_usuario = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'P'}))

class PacienteEditForm(PessoaForm):
    class Meta:
        model = Paciente
        exclude = ('razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'cnpj', 'user', 'tipo_usuario')

    email = forms.EmailField()
    username = forms.CharField(max_length=255)

class MedicoEditForm(PessoaForm):
    class Meta:
        model = Medico
        exclude = ('razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'cnpj', 'user', 'tipo_usuario', 'bairro', 'municipio', 'estado')

    email = forms.EmailField()
    username = forms.CharField(max_length=255)

class MedicoCreateForm(PessoaForm):
    class Meta:
        model = Medico
        exclude = ('razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'cnpj', 'user', 'tipo_usuario', 'clinica', 'bairro', 'municipio', 'estado')

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise forms.ValidationError('Já existe um usuário com este email.')
        return email

class AddMedicoToClinicaForm(forms.Form):

    medico = forms.ModelChoiceField(
        queryset=Medico.objects.filter(clinica__isnull=True), 
        label='Médico'
    )

class ClinicaEditForm(PessoaForm):
    class Meta:
        model = Clinica
        exclude = ('rg', 'cpf', 'orgao_emissor', 'enderecos', 'telefones', 'emails', 'contatos', 'user', 'tipo_usuario', 'bairro', 'municipio', 'estado')

    email = forms.EmailField()
    username = forms.CharField(max_length=255)


EnderecoMedicoFormSet = modelformset_factory(Endereco, exclude=('tipo', 'geocode'), can_delete=False)

class MedicoForm(PessoaForm):
    class Meta:
        model = Medico
        exclude = ('razao_social', 'enderecos', 'telefones', 'emails', 'contatos', 'cnpj', 'user', 'bairro', 'municipio', 'estado')

    inlines = [EnderecoMedicoFormSet]

    username = forms.CharField(label=u'Nome de usuário')
    email = forms.EmailField()
    password1 = forms.CharField(label=u'Senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirme a senha', widget=forms.PasswordInput())
    tipo_usuario = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'M'}))

    def save_formsets(self, formsets, obj_pessoa):
        super(MedicoForm, self).save_formsets(formsets, obj_pessoa)
        form = formsets[0][0]
        obj_pessoa.bairro = form.cleaned_data['bairro']
        obj_pessoa.municipio = form.cleaned_data['cidade']
        obj_pessoa.estado = form.cleaned_data['uf']
        obj_pessoa.save()


EnderecoClinicaFormSet = modelformset_factory(Endereco, exclude=('tipo', 'geocode'), can_delete=False)

class ClinicaForm(PessoaForm):
    class Meta:
        model = Clinica
        exclude = ('rg', 'cpf', 'orgao_emissor', 'enderecos', 'telefones', 'emails', 'contatos', 'user', 'bairro', 'municipio', 'estado')

    inlines = [EnderecoClinicaFormSet]

    username = forms.CharField(label=u'Nome de usuário')
    email = forms.EmailField()
    password1 = forms.CharField(label=u'Senha', widget=forms.PasswordInput())
    password2 = forms.CharField(label=u'Confirme a senha', widget=forms.PasswordInput())
    tipo_usuario = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'C'}))

    def save_formsets(self, formsets, obj_pessoa):
        super(ClinicaForm, self).save_formsets(formsets, obj_pessoa)
        form = formsets[0][0]
        obj_pessoa.bairro = form.cleaned_data['bairro']
        obj_pessoa.municipio = form.cleaned_data['cidade']
        obj_pessoa.estado = form.cleaned_data['uf']
        obj_pessoa.save()


class AgendaMedicoForm(forms.Form):
    especialidade = forms.ChoiceField(choices=Medico.ESPECIALIDADES)
    medico = forms.ModelChoiceField(queryset=Medico.objects.all())

class PerguntaForm(forms.Form):
    class Meta:
        exclude = ('data_hora',)

    conteudo = forms.CharField(widget=forms.Textarea, label=u'Pergunta:', required=True)

class RespostaForm(forms.Form):

    conteudo = forms.CharField(widget=forms.Textarea, label=u'Resposta:', required=True)

