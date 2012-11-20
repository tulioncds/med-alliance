# -*- coding: utf-8 -*-
import datetime
from uuid import uuid4

from django.conf import settings
from django.views.generic import FormView, View, UpdateView, TemplateView,\
                                 ListView, CreateView
from models import Paciente, Medico, Clinica, Consulta, UserProfile, Pergunta, Resposta
from forms import AdminEmailPacientesForm, PacienteEditForm, MedicoEditForm,\
                  ClinicaEditForm, AgendaMedicoForm, MedicoCreateForm,\
                  AddMedicoToClinicaForm, PerguntaForm, RespostaForm
from django.core.mail import send_mail, send_mass_mail
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.functional import lazy
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.http import HttpResponse

from registration.models import RegistrationProfile as rp

from schedule.models import Calendar, CalendarRelation
from schedule.utils import coerce_date_dict
from schedule.templatetags.scheduletags import querystring_for_date
from schedule.views import calendar_by_periods
from schedule.periods import Month

import requests
import json
from constants import API_URL
from pagseguro2.models import Payment, Notification, Transaction

class IdMixin(object):

    def get_context_data(self, **kwargs):
        context = super(IdMixin, self).get_context_data(**kwargs)
        if 'pk' in self.kwargs:
            user = self.get_user()
        return context

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])

class FaleConosco(IdMixin, FormView):
    form_class = AdminEmailPacientesForm
    template_name = 'core/fale_conosco.html'

    def post(self, request, *args, **kwargs):

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            titulo = self.request.POST['titulo']
            conteudo = self.request.POST['conteudo']

            admins = User.objects.filter(is_staff=True)
            email_list = []
            for admin in admins:
                email_list.append(admin.email)
            if len(email_list) > 0:
                send_mail(titulo, conteudo, self.get_user().email, email_list)

            messages.success(request, 'E-mail enviado com sucesso.')
            return redirect('home', pk=(request.user.pk))
        else:
            messages.error(request, 'E-mail não enviado, verifique campos')
            return redirect('home', pk=(request.user.pk))

class AdminEmailPacientes(FormView):
    form_class = AdminEmailPacientesForm
    template_name = 'core/emailpacientes.html'
    success_url = reverse_lazy('admin:%s_%s_changelist' %('core',  'paciente'),)

    def get_context_data(self, **kwargs):
        context = super(AdminEmailPacientes, self).get_context_data(**kwargs)
        pacientes = Paciente.objects.filter(pk__in=self.request.GET.getlist('ids'))
        email_list = []
        for paciente in pacientes:
            for email in paciente.emails.all():
                email_list.append(email.email)
        if len(email_list) > 0:
            context['emails'] = email_list
        return context

    def post(self, request, *args, **kwags):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            titulo = self.request.POST['titulo']
            conteudo = self.request.POST['conteudo']
            destinatarios = []
            destinatarios.append(self.request.POST['destinatario'])

            send_mail(titulo, conteudo, 'Med Alliance', destinatarios, fail_silently=False)

            messages.success(request, 'E-mails enviados com sucesso.')

            return HttpResponseRedirect(self.get_success_url())

class Home(IdMixin, TemplateView):

    def get_tipo_usuario(self):
        return self.get_user().profile.tipo_usuario

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        tipo_usuario = self.get_tipo_usuario()
        if tipo_usuario == 'M':
            medico = get_object_or_404(Medico, user=self.get_user())
            calendario = Calendar.objects.get_or_create_calendar_for_object(
                medico,
                name='Dr. %s' % medico.nome,
            )
            calendario_html = calendar_by_periods(
                self.request,
                calendario.slug,
                periods=[Month],
                template_name='schedule/calendar_compact_month.html',
            )
            context['calendario'] = calendario_html.content

        return context

    def get_template_names(self):
        tipo_usuario = self.get_tipo_usuario()
        if tipo_usuario == 'M':
            return ['core/home_medico.html']
        elif tipo_usuario == 'P':
            return ['core/home_paciente.html']
        elif tipo_usuario == 'C':
            return ['core/home_clinica.html']

class DeletePaciente(IdMixin, TemplateView):
    template_name = 'core/paciente_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.POST['id'])
        paciente_url = API_URL + 'paciente/%s' % user.profile.paciente.pk
        user_profile_url = API_URL + 'userprofile/%s' % user.profile.pk
        user_profile_payload = user.pk
        headers = {'content-type': 'application/json'}

        requests.delete(user_profile_url, data=json.dumps(user_profile_payload), headers=headers)
        requests.delete(paciente_url, headers=headers)

        messages.success(request, u'Usuário excluído com sucesso')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(DeletePaciente, self).get_context_data(**kwargs)
        context['paciente_id'] = kwargs['pk']
        return context

class DeleteMedico(IdMixin, TemplateView):
    template_name = 'core/medico_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.POST['id'])
        url = API_URL + 'medico/%s' % user.profile.medico.pk
        user_profile_url = API_URL + 'userprofile/%s' % user.profile.pk
        user_profile_payload = user.pk
        headers = {'content-type': 'application/json'}

        requests.delete(user_profile_url, data=json.dumps(user_profile_payload), headers=headers)
        requests.delete(url, headers=headers)

        messages.success(request, u'Usuário excluído com sucesso')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(DeleteMedico, self).get_context_data(**kwargs)
        context['medico_id'] = kwargs['pk']
        return context

class DeleteClinica(IdMixin, TemplateView):
    template_name = 'core/clinica_confirm_delete.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.POST['id'])
        url = API_URL + 'clinica/%s' % user.profile.clinica.pk
        user_profile_url = API_URL + 'userprofile/%s' % user.profile.pk
        user_profile_payload = user.pk
        headers = {'content-type': 'application/json'}

        requests.delete(user_profile_url, data=json.dumps(user_profile_payload), headers=headers)
        requests.delete(url, headers=headers)

        messages.success(request, u'Usuário excluído com sucesso')
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super(DeleteClinica, self).get_context_data(**kwargs)
        context['clinica_id'] = kwargs['pk']
        return context

class EditPaciente(IdMixin, UpdateView):
    template_name = 'core/edit_paciente.html'
    model = Paciente
    form_class = PacienteEditForm

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        return user.profile.paciente

    def get_initial(self):
        super(EditPaciente, self).get_initial()
        user = User.objects.get(pk=self.kwargs['pk'])
        self.initial = {'email': user.email, 'username': user.username}
        return self.initial

    def get_success_url(self):
        return lazy(reverse,str)('home', args=[self.get_user().pk])

    def get_context_data(self, **kwargs):
        context = super(EditPaciente, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        context['paciente_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        super(EditPaciente, self).form_valid(form)

        url = API_URL + 'paciente/%s' % self.request.POST['id']
        payload = {'nome': self.request.POST['nome'],\
                   'cpf': self.request.POST['cpf'],\
                   'rg': self.request.POST['rg'],\
                   'orgao_emissor': self.request.POST['orgao_emissor'],\
                   'username': self.request.POST['username'],\
                   'email': self.request.POST['email'],\
                   'id': self.request.POST['id'],
        }
        headers = {'content-type': 'application/json'}

        requests.put(url, data=json.dumps(payload), headers=headers)

        messages.success(self.request, 'Conta alterada com sucesso.')
        return HttpResponseRedirect(self.get_success_url())


class EditMedico(IdMixin, UpdateView):
    template_name = 'core/edit_medico.html'
    model = Medico
    form_class = MedicoEditForm

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        return user.profile.medico

    def get_initial(self):
        super(EditMedico, self).get_initial()
        user = User.objects.get(pk=self.kwargs['pk'])
        self.initial = {'email': user.email, 'username': user.username}
        return self.initial

    def get_success_url(self):
        return lazy(reverse,str)('home', args=[self.get_user().pk])

    def get_context_data(self, **kwargs):
        context = super(EditMedico, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        context['medico_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        super(EditMedico, self).form_valid(form)

        url = API_URL + 'medico/%s' % self.request.POST['id']
        payload = {'nome': self.request.POST['nome'],\
                   'cpf': self.request.POST['cpf'],\
                   'rg': self.request.POST['rg'],\
                   'orgao_emissor': self.request.POST['orgao_emissor'],
                   'crm': self.request.POST['crm'],\
                   'especialidade': self.request.POST['especialidade'],
                   'id': self.request.POST['id'],\
                   'username': self.request.POST['username'],\
                   'email': self.request.POST['email'],
        }
        headers = {'content-type': 'application/json'}

        requests.put(url, data=json.dumps(payload), headers=headers)

        messages.success(self.request, 'Conta Modificada.')
        return HttpResponseRedirect(self.get_success_url())


class CreateMedico(IdMixin, CreateView):
    template_name = 'core/create_medico.html'
    model = Medico
    form_class = MedicoCreateForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        form.instance.clinica = self.get_user().profile.clinica
        form.instance.tipo_usuario=UserProfile.USER_TYPES[1][0]
        form.instance.user = rp.objects.create_inactive_user(
            email, email,  unicode(uuid4()), None, send_email=True
        )
        form = super(CreateMedico, self).form_valid(form)
        messages.success(self.request, 'Médico adicionado.')
        return form

    def get_success_url(self):
        return lazy(reverse,str)('home', args=[self.get_user().pk])

class AddMedicoToClinica(IdMixin, FormView):
    template_name = 'core/add_medico_to_clinica.html'
    form_class = AddMedicoToClinicaForm

    def form_valid(self, form):
        super(AddMedicoToClinica, self).form_valid(form)
        id_medico = self.request.POST['medico']
        medico = get_object_or_404(Medico, pk=id_medico)
        medico.clinica = self.get_user().profile.clinica
        medico.save()
        messages.success(self.request, 'Médico atribuído à clínica.')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return lazy(reverse,str)('home', args=[self.get_user().pk])
    
    

# class DeleteMedicoFromClinica(IdMixin, FormView):
#    template_name = 'core/delete_medico_to_clinica.html'
#    form_class = DeleteMedicoToClinicaForm
#
 #   def form_valid(self, form):
  #      super(AddMedicoToClinica, self).form_valid(form)
   #     id_medico = self.request.POST['medico -']
    #    medico = get_object_or_404(Medico, pk=id_medico)
     #   medico.clinica = none
      #  medico.save()
       # messages.success(self.request, 'Médico excluido da clinica.')
        #return HttpResponseRedirect(self.get_success_url())

 #   def get_success_url(self):
 #       return lazy(reverse,str)('home', args=[self.get_user().pk])

    

class EditClinica(IdMixin, UpdateView):
    template_name = 'core/edit_clinica.html'
    model = Clinica
    form_class = ClinicaEditForm

    def get_object(self, queryset=None):
        user = User.objects.get(pk=self.kwargs['pk'])
        return user.profile.clinica

    def get_initial(self):
        super(EditClinica, self).get_initial()
        user = User.objects.get(pk=self.kwargs['pk'])
        self.initial = {'email': user.email, 'username': user.username}
        return self.initial

    def get_success_url(self):
        return lazy(reverse,str)('home', args=[self.get_user().pk])

    def get_context_data(self, **kwargs):
        context = super(EditClinica, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        context['clinica_id'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        super(EditClinica, self).form_valid(form)

        url = API_URL + 'clinica/%s' % self.request.POST['id']
        payload = {'nome': self.request.POST['nome'],\
                   'cnpj': self.request.POST['cnpj'],\
                   'razao_social': self.request.POST['razao_social'],
                   'id': self.request.POST['id'],\
                   'username': self.request.POST['username'],\
                   'email': self.request.POST['email']
        }
        headers = {'content-type': 'application/json'}

        requests.put(url, data=json.dumps(payload), headers=headers)

        messages.success(self.request, 'Conta Modificada.')
        return HttpResponseRedirect(self.get_success_url())

class Login(TemplateView):
    template_name = 'core/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None and not user.is_staff:
            if user.is_active:
                login(request, user)
                return redirect('home', pk=(user.pk))
            else:
                messages.error(request, 'Seu usuário ainda está inativo, acesse o email e siga as instruções!')
                return redirect('login')
        else:
            messages.error(request, 'Senha e/ou usuário inválido(s)!')
            return redirect('login')

        #Tentando usar API
        #url = API_URL + 'user/login/'
        #payload = {"username": username, "password": password}
        #headers = {'content-type': 'application/json'}

        #response = requests.post(url, data=json.dumps(payload), headers=headers)

        #if response.json['success']:
        #    return redirect('home', pk=response.json['pk'])
        #else:
        #    messages.error(request, 'Seu usuário ainda está inativo, acesse o email e siga as instruções!')
        #    return redirect('login')

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('login')

class AuthView(View):

    def get(self,request):

         if request.user.is_authenticated() and not request.user.is_staff:
             return redirect('home', pk=(request.user.pk))
         else:
             return redirect('login')

class FilterMixin(object):

    def get_queryset_filters(self):
        filters = {}
        for item in self.allowed_filters:
            if item in self.allowed_filters and item in self.request.GET:
                if item == 'clinica':
                    filters['clinica__nome'] = self.request.GET[item]
                elif item == 'nome':
                    filters['nome__icontains'] = self.request.GET[item]
                else:
                    filters[self.allowed_filters[item]] = self.request.GET[item]
        lista = [k for k,v in filters.iteritems() if v == 'todas' or v == '']
        for item in lista:
            del filters[item]
        return filters

    def get_queryset(self):
        return super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())

class MedicoList(IdMixin, FilterMixin, ListView):

    model = Medico
    paginate_by = 10

    allowed_filters = {
            'nome': 'nome',
            'especialidade': 'especialidade',
            'clinica': 'clinica',
    }

    def get_context_data(self, **kwargs):
        context = super(MedicoList, self).get_context_data(**kwargs)
        context['user'] = self.get_user()

        nomes_clinicas = []
        clinicas = Clinica.objects.all()
        for clinica in clinicas:
            nomes_clinicas.append(clinica.nome)
        context['clinicas'] = nomes_clinicas

        context['especialidades'] = Medico.get_especialidades()

        return context

class ClinicaMedicoList(IdMixin, FilterMixin, ListView):

    model = Medico
    paginate_by = 10

    allowed_filters = {
            'nome': 'nome',
            'especialidade': 'especialidade',
            'clinica': 'clinica',
    }

    def get_context_data(self, **kwargs):
        context = super(MedicoList, self).get_context_data(**kwargs)
        context['user'] = self.get_user()

        nomes_clinicas = []
        clinicas = Clinica.objects.all()
        for clinica in clinicas:
            nomes_clinicas.append(clinica.nome)
        context['clinicas'] = nomes_clinicas

        context['especialidades'] = Medico.get_especialidades()

        return context


class NovaConsulta(TemplateView):
    template_name = 'core/nova_consulta.html'

    def get_context_data(self, **kwargs):
        context = super(NovaConsulta, self).get_context_data(**kwargs)
        id_medico = self.request.GET.get('id_medico', None)
        medico = get_object_or_404(Medico, pk=id_medico)
        calendario = Calendar.objects.get_or_create_calendar_for_object(
            medico,
            name='Dr. %s' % medico.nome,
        )
        calendario_html = calendar_by_periods(
            self.request,
            calendario.slug,
            periods=[Month],
            template_name='schedule/calendar_month.html',
        )
        context['calendario'] = calendario_html.content
        context['medico'] = medico
        return context

class DadosPaciente(IdMixin, TemplateView):
    template_name = 'core/dados_paciente.html'

    def get_context_data(self, **kwargs):
        context = super(DadosPaciente, self).get_context_data(**kwargs)
        context['paciente'] = User.objects.get(pk=self.kwargs['pkpaciente'])
        context['user'] = User.objects.get(pk=self.kwargs['pkmedico'])
        return context

class Agendar(View, IdMixin):

    def get(self, request, pk):
        calendar_slug = request.GET.get('calendar_slug', None)
        calendar = get_object_or_404(Calendar, slug=calendar_slug)
        date = coerce_date_dict(request.GET)
        start = None
        end = None
        if date:
            try:
                start = datetime.datetime(**date)
                end = start + datetime.timedelta(minutes=30)
            except TypeError:
                raise Http404
            except ValueError:
                raise Http404
        cr = CalendarRelation.objects.get(calendar=calendar)
        medico = Medico.objects.get(pk=cr.object_id)
        paciente = Paciente.objects.get(user=self.get_user())
        consulta = None
        consulta = Consulta.objects.create(
            start=start,
            end=end,
            title=paciente.nome,
            description="Consulta para o paciente %s" %(paciente.nome),
            creator=self.get_user(),
            calendar=calendar,
            medico=medico,
            paciente=paciente,
        )
        #PAGSEGURO#
        if consulta:
           pay = Payment.objects.create(user=self.get_user())
           pay.add_item(medico.item, 1)
           redirect_url = self.request.META['HTTP_REFERER'] + '&result=ok%id_consulta={0}&id_pagamento={1}'.format(consulta.pk, pay.pk)
           pay.submit('http://globo.com')#Substituir por redirect_url quando em producao
           pay.save()
           consulta.pagamento = pay
           consulta.save()
           return HttpResponse(pay.client_url)
        response = redirect('day_calendar', calendar_slug=calendar.slug)
        response['Location'] += querystring_for_date(start)
        return response


class PerfilMedico(IdMixin, TemplateView):
    template_name = 'core/perfil_medico.html'

    def get_context_data(self, **kwargs):
        context = super(PerfilMedico, self).get_context_data(**kwargs)
        context['medico'] = self.get_user().profile.medico
        context['user'] = self.get_user()
        context['GOOGLE_KEY'] = settings.GOOGLE_KEY
        return context

class EnviarPergunta(IdMixin, FormView):
    form_class = PerguntaForm
    template_name = 'core/pergunta.html'

    def get_context_data(self, **kwargs):
        context = super(EnviarPergunta, self).get_context_data(**kwargs)
        context['medico'] = Medico.objects.get(pk=self.request.GET['id_medico'])
        return context

    def form_valid(self, form):
        medico = Medico.objects.get(pk=self.request.POST['medico-questionado'][0])
        paciente = User.objects.get(pk=self.kwargs['pk']).profile.paciente
        conteudo = self.request.POST['conteudo']
        agora = datetime.datetime.now()
        Pergunta.objects.create(medico=medico, paciente=paciente, conteudo=conteudo, data_hora=agora)
        messages.success(self.request, 'Pergunta enviada com sucesso.')
        return redirect('medico_profile', pk=(medico.user.pk))

    def form_invalid(self, form):
        messages.error(request, 'Pergunta não enviada!')
        return self.render_to_response(self.get_context_data(form=form))

class Responder(IdMixin, FormView):
    form_class = RespostaForm
    template_name = 'core/resposta_list.html'

    def get_context_data(self, **kwargs):
        context = super(Responder, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        context['perguntas'] = Pergunta.objects.filter(medico=self.get_user().profile.medico, lida=False)
        return context

    def form_valid(self, form):
        medico = User.objects.get(pk=self.request.POST['medico_pk']).profile.medico
        paciente = Paciente.objects.get(pk=self.request.POST['paciente_pk'])
        pergunta = Pergunta.objects.get(pk=self.request.POST['pergunta_pk'])
        pergunta.lida = True
        pergunta.save()
        conteudo = self.request.POST['conteudo']
        agora = datetime.datetime.now()
        Resposta.objects.create(pergunta=pergunta, medico=medico, paciente=paciente, data_hora=agora, conteudo=conteudo)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return lazy(reverse,str)('respostas', args=[self.get_user().pk])

class VerRespostas(IdMixin, TemplateView):
    template_name = 'core/paciente_respostas.html'

    def get_context_data(self, **kwargs):
        context = super(VerRespostas, self).get_context_data(**kwargs)
        context['user'] = self.get_user()
        context['respostas'] = Resposta.objects.filter(paciente=self.get_user().profile.paciente)
        return context

@csrf_exempt
def notification(request):
    if request.POST['notificationCode']:
        incoming_notification = Notification(code=request.POST['notificationCode'])
        incoming_notification.save()
        incoming_notification.check
    elif request.POST['StatusTransacao']:
        incoming_transaction = Transaction(status=request.POST['StatusTransacao'])
        incoming_transaction.save()
    return HttpResponse("OK", mimetype="text/plain")
