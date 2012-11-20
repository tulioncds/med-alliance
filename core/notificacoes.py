# -*- conding: utf-8 -*-
from datetime import *
from django.core.mail import send_mail, send_mass_mail
from dateutil.relativedelta import *
import threading
from models import Consulta, Paciente
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

@run_in_thread
def _enviar_email(subject, message, remetente, destinatario):
    send_mail(subject, message, remetente, destinatario)

def _validar_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def _coletar_consultas_iminentes():
    return Consulta.objects.filter(start__gte=datetime.today()).filter(start__lte=datetime.today()+relativedelta(days=+1))

def notificar_consultas_iminentes():
    subject = 'Lembrete de consulta marcada'
    message = u'A equipe da MedAlliance gostaria de lembrar que o Sr(a). tem uma consulta marcada para o dia {0} as {1}'
    sender = 'MedAlliance'

    consultas = _coletar_consultas_iminentes()

    for consulta in consultas:
        email_paciente = Paciente.objects.get(pk=consulta.paciente_id).user.email
        if _validar_email(email_paciente):
            destinatario = [email_paciente]
            formatted_message = message.format(consulta.start.date().strftime('%d/%m/%y'), consulta.start.strftime('%H:%M'))
            _enviar_email(subject, formatted_message, sender, destinatario)
