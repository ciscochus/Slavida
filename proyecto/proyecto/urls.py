#encoding:utf-8

from django.conf.urls import patterns, include, url

# Librerias para añadir los directorios estáticos y media
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	#las urls van con prioridad siendo la primera la prioridad mas alta, es decir, WANO NO LO TOQUES
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'proyecto.views.home', name='home'),
    # url(r'^proyecto/', include('proyecto.foo.urls')),
    #Página de inicio
    url(r'^$','slavida.views.inicio'),
    #Página de votación
    url(r'^vota/$', 'slavida.views.vota'),
    #Página de las conversaciones
    url(r'^mensajes/$', 'slavida.views.mensajes'),
    #Página de las conversaciones
    url(r'^conversacion', 'slavida.views.conversacion'),
    #URL editar perfil
    url(r'^editperfil/$','slavida.views.edit_perfil'),
    #URL editar perfil
    url(r'^completarregistro/$','slavida.views.completarregistro'),
    #URL página principal 
    url(r'^principal/$','slavida.views.principal'),
    #URL cerrar sesión
     url(r'^logout/$','slavida.views.cerrar_sesion'),
    #Página archivos
    url(r'^misarchivos/$','slavida.views.box'),
    url(r'^misarchivos/(?P<pk>.*)/delete$','slavida.views.remove_archivo'),
    #Página para mostrar archivos de forma individual
    url(r'^misarchivos/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
    #Página diario
    url(r'^midiario/$','slavida.views.diario'),
    url(r'^midiario/(?P<pk>[0-9]+)/delete$','slavida.views.remove_diario'),
    url(r'^midiario/(?P<pk>[0-9]+)/$','slavida.views.edit_diario'),
    #Página agenda
    url(r'^miagenda/$','slavida.views.agenda'),
    url(r'^miagenda/(?P<pk>[0-9]+)/delete$','slavida.views.remove_evento'),
    url(r'^miagenda/(?P<pk>[0-9]+)/$','slavida.views.edit_evento'),
    #Página usuario
    url(r'^(?P<user>[\w|\W]+)/$', 'slavida.views.perfil'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
