#coding: utf-8
from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',
    (r'^pagseguro/notification/$', 'pagseguro2.views.notification'),
    url(r'^transacoes/$', 'pagseguro2.views.lista_compras', name="lista_compras"),
    url(r'^compras/$', 'pagseguro2.views.lista_todas', name="lista_todas"),
    url(r'^pagseguro/comprar/(?P<slug>.*)/"$', 'pagseguro2.views.comprar', name="pagseguro_comprar"),
    url(r'^pag-nao-realizados/$', 'pagseguro2.views.pag_nao_realizados', name="pag_nao_realizados"),
    url(r'^finalizar-pagamento/(?P<pagamento>.*)/$', 'pagseguro2.views.finalizar_pagamento', name="finalizar_pagamento"),
)
