# -*- conding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from core.notificacoes import notificar_consultas_iminentes

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        notificar_consultas_iminentes()
