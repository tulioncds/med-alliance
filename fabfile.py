# *-* coding: utf-8 *-*
#TODOS OS SOs TERAO QUE TER GAWK INSTALADO

from partec_utils.fabfile import Fabric
from fabric.api import *
from fabric.contrib.files import sed, append, contains, comment, uncomment
from fabriclassed import initialize
import os

class MedAllianceFabric(Fabric):

    def fab_primeiro_deploy(self):
        super(MedAllianceFabric, self).fab_primeiro_deploy()
        self.fab_criar_crons

    def fab_deploy(self):
        super(MedAllianceFabric, self).fab_deploy()
        self.fab_criar_crons

    def fab_criar_crons(self):
        ''' Insere tarefa definida em ../cron/cronconf no crontab do servidor '''
        crontab_location = '/etc/crontab'
        with cd(env.code_root):
            if os.path.exists('cron'):
                from cron.cronconf import CRONS
                import re
                sudo('chmod 646 ' + crontab_location)

                for cron in CRONS:

                    if cron['comando_de_projeto'] and not cron['django_management']:
                        linha_cron = cron['tempo'] + ' ' + cron['usuario'] + ' ' + env.code_root +'/'+ cron['comando']
                    else:
                        if cron['comando_de_projeto'] and cron['django_management']:
                            linha_cron =  cron['tempo'] + ' ' + cron['usuario'] + ' /usr/bin/python ' + env.code_root + '/' + cron['comando'] + ' --settings=med_alliance.settings.' + env.ambiente
                        else:
                            linha_cron =  cron['tempo'] + ' ' + cron['usuario'] + ' ' + cron['comando']
                    if cron['ligado']:
                        if not contains(crontab_location, re.escape(linha_cron)):
                            append(crontab_location, linha_cron, use_sudo=False)
                        else:
                            uncomment(crontab_location, re.escape(linha_cron))
                    else:
                        if contains(crontab_location, re.escape(linha_cron)):
                            comment(crontab_location, re.escape(linha_cron))

                sudo('chmod 644 ' + crontab_location)

__all__ = initialize(MedAllianceFabric(), __name__)
