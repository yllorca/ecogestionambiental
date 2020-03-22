from django.conf.urls import url
from .views import PanelView, LogoutView, DetalleReclamoView, EnviarReclamoView, \
    form_enviar_reclamo_ajax, update_reclamo_ajax, respuesta_reclamo_ajax, ListarClientesView, \
    DetalleClienteView, crear_cliente_ajax, update_cliente_ajax, ContactoPanelView, \
    ServiciosPanelView, ServiciosEditarView, ServicioCrearView, EquipoListView, EquipoCreateView, \
    EquipoEditView, CertificacionListView, CertificacionCreateView, CertificacionEditView, ServiciosDeleteView, \
    EquipoDeleteView, CertificacionDeleteView, ContactonDeleteView

urlpatterns = [
    url(r'^$', PanelView, name='panel'),
    url(r'^solicitud/(?P<id>\d+)$', DetalleReclamoView, name="detalle-reclamo"),
    url(r'^solicitud/nuevo/$', EnviarReclamoView, name="crear-reclamo"),
    url(r'^form/form_ajax$', form_enviar_reclamo_ajax, name='form-reclamo--ajax'),
    url(r'^form/reclamo/form_ajax/(?P<id>\d+)/$', update_reclamo_ajax, name='form-update-reclamo-ajax'),
    url(r'^form/respuesta/form_ajax/$', respuesta_reclamo_ajax, name='form-respuesta-reclamo-ajax'),

    url(r'^clientes/$', ListarClientesView, name="listar-cliente"),
    url(r'^cliente/(?P<id>\d+)$', DetalleClienteView, name="detalle-cliente"),
    url(r'^cliente/nuevo/form_ajax/$', crear_cliente_ajax, name='form-nuevo-cliente'),
    url(r'^cliente/editar/form_ajax/(?P<id>\d+)/$', update_cliente_ajax, name='form-update-cliente-ajax'),

    url(r'^modulo/contactos/$', ContactoPanelView, name="listar-contactos"),
    url(r'^modulo/contactos/eliminar/(?P<id>\d+)$', ContactonDeleteView, name="eliminar-contacto"),

    url(r'^modulo/servcios/$', ServiciosPanelView, name="listar-servicios"),
    url(r'^modulo/servicio/(?P<id>\d+)$', ServiciosEditarView, name="detalle-servicio"),
    url(r'^modulo/servicio/eliminar/(?P<id>\d+)$', ServiciosDeleteView, name="eliminar-servicio"),
    url(r'^modulo/servicio/nuevo/$', ServicioCrearView, name="crear-servicio"),

    url(r'^modulo/equipo/$', EquipoListView, name="listar-equipo"),
    url(r'^modulo/equipo/nuevo/$', EquipoCreateView, name="crear-equipo"),
    url(r'^modulo/equipo/(?P<id>\d+)$', EquipoEditView, name="editar-equipo"),
    url(r'^modulo/equipo/eliminar/(?P<id>\d+)$', EquipoDeleteView, name="eliminar-equipo"),

    url(r'^modulo/certificaciones/$', CertificacionListView, name="listar-certificacion"),
    url(r'^modulo/certificaciones/nuevo/$', CertificacionCreateView, name="crear-certificacion"),
    url(r'^modulo/certificacion/(?P<id>\d+)$', CertificacionEditView, name="editar-certificacion"),
    url(r'^modulo/certificacion/eliminar/(?P<id>\d+)$', CertificacionDeleteView, name="eliminar-certificado"),

    url(r'^salir/$', LogoutView, name="salir"),
]
