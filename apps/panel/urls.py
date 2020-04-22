from django.conf.urls import url
from .views import PanelView, LogoutView, DetalleReclamoView, EnviarReclamoView, \
    form_enviar_reclamo_ajax, update_reclamo_ajax, respuesta_reclamo_ajax, ListarClientesView, \
    DetalleClienteView, crear_cliente_ajax, update_cliente_ajax, ContactoPanelView, \
    ServiciosPanelView, ServiciosEditarView, ServicioCrearView, EquipoListView, EquipoCreateView, \
    EquipoEditView, CertificacionListView, CertificacionCreateView, CertificacionEditView, ServiciosDeleteView, \
    EquipoDeleteView, CertificacionDeleteView, ContactonDeleteView, ListarUsuarios, crear_usuario_ajax, \
    update_usuario_ajax, DetalleUsuarioView, ClientesDeleteView, ListarInformesView, InformeEditView, \
    InformeCreateView, ListarInformesClienteView, login_success

urlpatterns = [

    url(r'login_success/$', login_success, name='login_success'),

    url(r'^solicitudes/$', PanelView, name="listar-solicitudes"),
    url(r'^solicitud/(?P<id>\d+)$', DetalleReclamoView, name="detalle-reclamo"),
    url(r'^solicitud/nuevo/$', EnviarReclamoView, name="crear-reclamo"),
    url(r'^form/form_ajax$', form_enviar_reclamo_ajax, name='form-reclamo--ajax'),
    url(r'^form/reclamo/form_ajax/(?P<id>\d+)/$', update_reclamo_ajax, name='form-update-reclamo-ajax'),
    url(r'^form/respuesta/form_ajax/$', respuesta_reclamo_ajax, name='form-respuesta-reclamo-ajax'),

    url(r'^$', ListarInformesView, name='panel'),
    url(r'^my/informes/$', ListarInformesClienteView, name="listar-informes-clientes"),
    url(r'^informe/(?P<id>\d+)$', InformeEditView, name="editar-informe"),
    url(r'^informe/nuevo/$', InformeCreateView, name="crear-informe"),

    url(r'^usuarios/$', ListarUsuarios, name="listar-usuarios"),
    url(r'^usuarios/nuevo/form_ajax/$', crear_usuario_ajax, name="form-crear-usuario-por-ajax"),
    url(r'^usuario/(?P<id>\d+)$', DetalleUsuarioView, name="detalle-usuario"),
    url(r'^usuarios/editar/form_ajax/(?P<id>\d+)/$', update_usuario_ajax, name='form-update-usuario-ajax'),
    # url(r'^usuarios/eliminar/(?P<id>\d+)$', UsuariosDeleteView, name="eliminar-usuario"),

    url(r'^clientes/$', ListarClientesView, name="listar-cliente"),
    url(r'^cliente/(?P<id>\d+)$', DetalleClienteView, name="detalle-cliente"),
    url(r'^cliente/nuevo/form_ajax/$', crear_cliente_ajax, name='form-nuevo-cliente'),
    url(r'^cliente/editar/form_ajax/(?P<id>\d+)/$', update_cliente_ajax, name='form-update-cliente-ajax'),
    url(r'^cliente/eliminar/(?P<id>\d+)/$', ClientesDeleteView, name='eliminar-cliente'),

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
