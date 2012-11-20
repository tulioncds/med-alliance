# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication, SessionAuthentication
from models import Paciente, Medico, Consulta, Clinica, UserProfile
from tastypie import fields
from django.contrib.auth.models import User
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.serializers import Serializer
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden

from django.core.urlresolvers import reverse

class UserProfileResource(ModelResource):

    class Meta:
        queryset = UserProfile.objects.all()
        authorization= Authorization()

    def obj_delete(self, request=None, **kwargs):
        user = User.objects.get(pk=request.raw_post_data)
        user.delete()
        return super(UserProfileResource, self).obj_delete(request, **kwargs)

class UserResource(ModelResource):

    #profile = fields.ToOneField('UserProfileResource', 'profile')

    class Meta:
        queryset = User.objects.all()
        fields = ['email', 'username',]
        allowed_methods = ['get', 'post',]
        resouce_name = 'user'
        authorization = Authorization()

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resouce_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.raw_post_data, format=request.META.get('CONTENT-TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)

        if user and not user.is_staff:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True,
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': u'Usuário desabilitado',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'Usuário e/ou senha incorretos',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)

class PacienteResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Paciente.objects.all()
        authorization = Authorization()
        fields = ['nome',]
        filtering = {
                'nome': ('exact', 'startswith',),
                'email': ('exact', 'startswith',),
        }

    def obj_update(self, bundle, request=None, skip_errors=False, **kwargs):
        p = Paciente.objects.get(id=bundle.data['id'])
        if p.user.username != bundle.data['username']:
            p.user.username = bundle.data['username']
        if p.user.email != bundle.data['email']:
            p.user.email = bundle.data['email']
        p.user.save()

        bundle.data.pop('email')
        bundle.data.pop('username')

        return super(PacienteResource, self).obj_update(bundle, request, skip_errors, **kwargs)

class MedicoResource(ModelResource):

    class Meta:
        queryset = Medico.objects.all()
        authorization = Authorization()
        fields = ['nome', 'especialidade', 'crm']
        filtering = {
                'nome': ('exact', 'startswith',),
                'clinica': ('exact', 'startswith',),
                'especialidade': ('exact', 'startswith',),
        }

    def obj_update(self, bundle, request=None, skip_errors=False, **kwargs):
        m = Medico.objects.get(id=bundle.data['id'])
        if m.user.username != bundle.data['username']:
            m.user.username = bundle.data['username']
        if m.user.email != bundle.data['email']:
            m.user.email = bundle.data['email']
        m.user.save()

        bundle.data.pop('email')
        bundle.data.pop('username')

        return super(MedicoResource, self).obj_update(bundle, request, skip_errors, **kwargs)

class ConsultaResource(ModelResource):

    class Meta:
        queryset = Consulta.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
                'title': ('exact', 'startswith',),
                'start': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
                'end': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }

    medico = fields.ForeignKey(MedicoResource, 'medico')
    paciente = fields.ForeignKey(MedicoResource, 'paciente')

class ClinicaResource(ModelResource):
    class Meta:
        queryset = Clinica.objects.all()
        authorization = Authorization()

    def obj_update(self, bundle, request=None, skip_errors=False, **kwargs):
        c = Clinica.objects.get(id=bundle.data['id'])
        if c.user.username != bundle.data['username']:
            c.user.username = bundle.data['username']
        if c.user.email != bundle.data['email']:
            c.user.email = bundle.data['email']
        c.user.save()

        bundle.data.pop('email')
        bundle.data.pop('username')

        return super(ClinicaResource, self).obj_update(bundle, request, skip_errors, **kwargs)
