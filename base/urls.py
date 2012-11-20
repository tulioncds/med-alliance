from django.conf.urls.defaults import patterns, include, url
from views import PessoaCreateView, PessoaUpdateView, PessoaDeleteView, PessoaListView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('')
if settings.DEBUG:
#    #django 1.3, static files
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    # media
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )

urlpatterns += patterns('',
     url(r'^add/$', PessoaCreateView.as_view() , name='pessoa_cadastro'),
     url(r'^$', PessoaListView.as_view() , name='pessoa_list'),
     url(r'^editar/(?P<pk>\d+)$', PessoaUpdateView.as_view() , name='pessoa_editar'),
     url(r'^delete/(?P<pk>\d+)$', PessoaDeleteView.as_view() , name='pessoa_delete'),

#     url(r'^salvar/$', pessoa_salvar , name='pessoa_salvar'),
    # url(r'^cadastro_pessoa/', include('cadastro_pessoa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
