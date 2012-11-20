# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.contrib.sites.models import Site
from django.conf import settings

from registration.models import RegistrationProfile as rp
from core.models import Paciente, Medico, Clinica, UserProfile
from base.models import Endereco
from pagseguro2.models import Item

class Command(NoArgsCommand):
    help = "Cria usuarios de medicos e pacientes para teste do sistema"

    def handle_noargs(self, **options):
        Site.objects.create(domain='http://localhost:8000', name='Localhost', pk=settings.SITE_ID)
        item = Item.objects.create(description='consulta', amount='120.00')
        u1 = rp.objects.create_inactive_user(
            'paciente1', 'p1@p.com', '123', None, send_email=False
        )
        u2 = rp.objects.create_inactive_user(
            'paciente2', 'p2@p.com', '123', None, send_email=False
        )
        u3 = rp.objects.create_inactive_user(
            'medico1', 'm1@p.com', '123', None, send_email=False
        )
        u4 = rp.objects.create_inactive_user(
            'medico2', 'm2@p.com', '123', None, send_email=False
        )
        u5 = rp.objects.create_inactive_user(
            'medico3', 'm3@p.com', '123', None, send_email=False
        )
        u6 = rp.objects.create_inactive_user(
            'medico4', 'm4@p.com', '123', None, send_email=False
        )
        u7 = rp.objects.create_inactive_user(
            'clinica1', 'c1@p.com', '123', None, send_email=False
        )
        u8 = rp.objects.create_inactive_user(
            'clinica2', 'c2@p.com', '123', None, send_email=False
        )

        e1 = Endereco.objects.create(logradouro='Rua Mamanguape', numero='665', complemento='apt 901', bairro='Boa Viagem', cep='51020-250', cidade='Recife', uf='Pernambuco')
        e2 = Endereco.objects.create(logradouro=u'Rua Antônio Falcão', numero='322', bairro='Boa Viagem', cidade='Recife', uf='Pernambuco')
        e3 = Endereco.objects.create(logradouro='Rua Princesa Izabel', numero='129', bairro='Santo Amaro', cidade='Recife', uf='Pernambuco')
        e4 = Endereco.objects.create(logradouro='Av. Rui Barbosa', numero='472', bairro='Graças', cidade='Recife', uf='Pernambuco')
        e5 = Endereco.objects.create(logradouro='Rua Augusto dos Anjos', numero='80', bairro=u'Heliópolis', cidade='Garanhuns', uf='Pernambuco')

        users = [u1,u2,u3,u4,u5,u6,u7,u8]
        for u in users:
            u.is_active = True
            u.save()

        p1 = Paciente.objects.create(
            nome='paciente1',
            cpf='752.654.626-00',
            rg='12345',
            orgao_emissor='SSP',
            user=u1,
            tipo_usuario=UserProfile.USER_TYPES[0][0],
        )
        p2 = Paciente.objects.create(
            nome='paciente2',
            cpf='144.784.541-24',
            rg='22345',
            orgao_emissor='SSP',
            user=u2,
            tipo_usuario=UserProfile.USER_TYPES[0][0],
        )
        c1 = Clinica.objects.create(
            nome='clinica1',
            cnpj='55.498.346/0001-53',
            razao_social='clinica1',
            user=u7,
            tipo_usuario=UserProfile.USER_TYPES[2][0],
            bairro=u'Graças',
            municipio='Recife',
            estado='Pernambuco',
        )
        c1.enderecos.add(e4)
        c1.save()

        c2 = Clinica.objects.create(
            nome='clinica2',
            cnpj='33.962.564/0001-64',
            razao_social='clinica2',
            user=u8,
            tipo_usuario=UserProfile.USER_TYPES[2][0],
            bairro=u'Heliópolis',
            municipio='Garanhuns',
            estado='Pernambuco',
        )
        c2.enderecos.add(e5)
        c2.save()

        m1 = Medico.objects.create(
            nome='medico1',
            cpf='110.372.873-39',
            rg='32345',
            orgao_emissor='SSP',
            user=u3,
            tipo_usuario=UserProfile.USER_TYPES[1][0],
            crm='21321',
            especialidade=Medico.ESPECIALIDADES[0][0],
            clinica=c1,
            bairro=u'Boa Viagem',
            municipio='Recife',
            estado='Pernambuco',
            item=item,
        )
        m1.enderecos.add(e1)
        m1.save()
        m2 = Medico.objects.create(
            nome='medico2',
            cpf='705.416.197-13',
            rg='42345',
            orgao_emissor='SSP',
            user=u4,
            tipo_usuario=UserProfile.USER_TYPES[1][0],
            crm='23321',
            especialidade=Medico.ESPECIALIDADES[1][0],
            clinica=c2,
            bairro=u'Boa Viagem',
            municipio='Recife',
            estado='Pernambuco',
            item=item,
        )
        m2.enderecos.add(e2)
        m2.save()

        m3 = Medico.objects.create(
            nome='medico3',
            cpf='717.608.331-26',
            rg='52345',
            orgao_emissor='SSP',
            user=u5,
            tipo_usuario=UserProfile.USER_TYPES[1][0],
            crm='41321',
            especialidade=Medico.ESPECIALIDADES[0][0],
            clinica=c2,
            bairro=u'Santo Amaro',
            municipio='Recife',
            estado='Pernambuco',
            item=item,
        )
        m3.enderecos.add(e3)
        m3.save()

        m4 = Medico.objects.create(
            nome='medico4',
            cpf='366.616.203-74',
            rg='62345',
            orgao_emissor='SSP',
            user=u6,
            tipo_usuario=UserProfile.USER_TYPES[1][0],
            crm='51321',
            especialidade=Medico.ESPECIALIDADES[2][0],
            clinica=c2,
            bairro=u'Heliópolis',
            municipio='Garanhuns',
            estado='Pernambuco',
            item=item,
        )
        m4.enderecos.add(e5)
        m4.save()
