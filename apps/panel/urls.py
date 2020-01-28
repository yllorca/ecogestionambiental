from django.conf.urls import url
from .views import PanelView, LogoutView, DetalleReclamoView, EnviarReclamoView, \
    form_enviar_reclamo_ajax, update_reclamo_ajax, respuesta_reclamo_ajax

urlpatterns = [
    url(r'^$', PanelView, name='panel'),
    url(r'^reclamos/(?P<id>\d+)$', DetalleReclamoView, name="detalle-reclamo"),
    url(r'^reclamos/nuevo/$', EnviarReclamoView, name="crear-reclamo"),
    url(r'^form/form_ajax$', form_enviar_reclamo_ajax, name='form-reclamo--ajax'),
    url(r'^form/reclamo/form_ajax/(?P<id>\d+)/$', update_reclamo_ajax, name='form-update-reclamo-ajax'),
    url(r'^form/respuesta/form_ajax/$', respuesta_reclamo_ajax, name='form-respuesta-reclamo-ajax'),
    url(r'^salir/$', LogoutView, name="salir"),
]
