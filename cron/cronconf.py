# -*- coding: utf-8 -*-
#   Autor: Wilberto Filho
#   ligado = Indica se o cron deve estar ativo ou não no servidor;
#   comando_de_projeto = indica se o comando deve ser executado dentro da pasta
#   do projeto ou não;
#   django_management = indica se no final do comando deverá ser adicionado
#   "--settings=settings.X" onde X é o settings do ambiente usado no fabric
#   tempo = A configuração de tempo de execução do cron(MIN HOUR DOM MON DOW)
#   usuario = O usuário que será utilizado pelo cron
#   comando = O comando a ser executado pelo cron, caso não esteja no $PATH,
#   indicar o comando com o caminho completo
#
#
#   Para adicionar outro cron, basta adicionar outro dicionário com as mesmas
#   chaves e os valores desejados

CRONS = [
        {
            'ligado': True,
            'comando_de_projeto': True,
            'django_management': True,
            'tempo': '0 0 0 0 *',
            'usuario': 'root',
            'comando': 'manage.py aviso_proximidade_consulta',
        },
]
