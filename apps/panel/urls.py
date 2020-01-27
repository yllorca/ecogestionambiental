from django.conf.urls import url
from .views import PanelView, LogoutView, DetalleReclamoView, EnviarReclamoView, form_enviar_reclamo_ajax

urlpatterns = [
    url(r'^$', PanelView, name='panel'),
    url(r'^reclamos/(?P<id>\d+)$', DetalleReclamoView, name="detalle-reclamo"),
    url(r'^reclamos/nuevo/$', EnviarReclamoView, name="crear-reclamo"),
    url(r'^form/form_ajax$', form_enviar_reclamo_ajax, name='form-reclamo--ajax'),
    url(r'^salir/$', LogoutView, name="salir"),
]
