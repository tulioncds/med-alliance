from django.conf.urls import patterns, include, url

from core.views import AdminEmailPacientes, Home, AuthView,\
                       Login, EditPaciente, EditMedico,\
                       MedicoList, Logout, DeletePaciente,\
                       DeleteMedico, DeleteClinica, EditClinica,\
                       FaleConosco, NovaConsulta, Agendar, PerfilMedico,\
                       CreateMedico, AddMedicoToClinica, DadosPaciente,\
                       EnviarPergunta, Responder, VerRespostas, notification

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from tastypie.api import Api
from core.api import PacienteResource, MedicoResource, ConsultaResource, ClinicaResource,\
                     UserResource, UserProfileResource

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(PacienteResource())
v1_api.register(MedicoResource())
v1_api.register(ConsultaResource())
v1_api.register(ClinicaResource())
v1_api.register(UserResource())
v1_api.register(UserProfileResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^med_alliance/', include('med_alliance.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/pacientes_email/$', AdminEmailPacientes.as_view(), name='admin_email_pacientes'),
    url(r'^faleconosco/(?P<pk>\d+)/$', FaleConosco.as_view(), name='fale_conosco'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', csrf_protect(Login.as_view()), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^home/(?P<pk>\d+)/$', login_required(Home.as_view()), name='home'),
    url(r'^home/(?P<pk>\d+)/medicos/$', login_required(MedicoList.as_view()), name='medico_list'),
    url(r'^consulta/(?P<pk>\d+)/nova/$', login_required(NovaConsulta.as_view()), name='nova_consulta'),
    url(r'^pergunta/(?P<pk>\d+)/nova/$', login_required(EnviarPergunta.as_view()), name='nova_pergunta'),
    url(r'^mensagens/medico/(?P<pk>\d+)/$', login_required(Responder.as_view()), name='respostas'),
    url(r'^mensagens/paciente/(?P<pk>\d+)/$', login_required(VerRespostas.as_view()), name='ver_respostas'),
    url(r'^medico/(?P<pkmedico>\d+)/dadospaciente/(?P<pkpaciente>\d+)/$', login_required(DadosPaciente.as_view()), name='dados_paciente'),
    url(r'^perfil/medico/(?P<pk>\d+)/$', login_required(PerfilMedico.as_view()), name='medico_profile'),
    url(r'^excluir/paciente/(?P<pk>\d+)/$', login_required(DeletePaciente.as_view()), name='delete_paciente'),
    url(r'^editar/paciente/(?P<pk>\d+)/$', login_required(EditPaciente.as_view()), name='edit_paciente'),
    url(r'^excluir/medico/(?P<pk>\d+)/$', login_required(DeleteMedico.as_view()), name='delete_medico'),
    url(r'^editar/medico/(?P<pk>\d+)/$', login_required(EditMedico.as_view()), name='edit_medico'),
    url(r'^clinica/(?P<pk>\d+)/adicionar/medico/$', login_required(CreateMedico.as_view()), name='create_medico'),
    url(r'^clinica/(?P<pk>\d+)/atribuir/medico/$', login_required(AddMedicoToClinica.as_view()), name='add_medico_to_clinica'),
    url(r'^excluir/clinica/(?P<pk>\d+)/$', login_required(DeleteClinica.as_view()), name='delete_clinica'),
    url(r'^editar/clinica/(?P<pk>\d+)/$', login_required(EditClinica.as_view()), name='edit_clinica'),
    url(r'^agendar/(?P<pk>\d+)/$', login_required(Agendar.as_view()), name='agendar'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^contas/', include('registration.backends.default.urls')),
    url(r'^schedule/', include('schedule.urls')),
    url(r'^pagseguro/notifications', notification),
    url(r'^$', AuthView.as_view(), name='auth'),
)
