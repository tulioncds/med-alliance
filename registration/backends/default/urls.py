"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register


from core.forms import PacienteForm, MedicoForm, ClinicaForm


urlpatterns = patterns('',
                       url(r'^ativacao/completa/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^ativar/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_ativar'),
                       url(r'^cadastro/paciente/$',
                           register,
                           {
                            'backend': 'core.backends.RegistrationController',
                            'form_class': PacienteForm,
                            'template_name': 'registration/registration_paciente.html',
                           },
                           name='registration_paciente'),
                       url(r'^cadastro/medico/$',
                           register,
                           {
                            'backend': 'core.backends.RegistrationController',
                            'form_class': MedicoForm,
                            'template_name': 'registration/registration_medico.html',
                           },
                           name='registration_medico'),
                       url(r'^cadastro/clinica/$',
                           register,
                           {
                            'backend': 'core.backends.RegistrationController',
                            'form_class': ClinicaForm,
                            'template_name': 'registration/registration_clinica.html',
                           },
                           name='registration_clinica'),
                       url(r'^cadastro/$',
                           direct_to_template,
                           {'template': 'registration/choose_type.html'},
                           name='registration_cadastro'),
                       url(r'^cadastro/completo/paciente/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete_paciente.html'},
                           name='registration_complete_paciente'),
                       url(r'^cadastro/completo/medico/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete_medico.html'},
                           name='registration_complete_medico'),
                       url(r'^cadastro/completo/clinica/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete_clinica.html'},
                           name='registration_complete_clinica'),
                       url(r'^cadastro/fechado/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_fechado'),
                       (r'', include('registration.auth_urls')),
                       )
