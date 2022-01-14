from django.conf.urls import url
from django.urls import path

from .views import PanelView, LogoutView, DetalleReclamoView, EnviarReclamoView, \
    form_enviar_reclamo_ajax, update_reclamo_ajax, respuesta_reclamo_ajax, ListarClientesView, \
    DetalleClienteView, crear_cliente_ajax, update_cliente_ajax, ContactoPanelView, \
    ServiciosPanelView, ServiciosEditarView, ServicioCrearView, EquipoListView, EquipoCreateView, \
    EquipoEditView, CertificacionListView, CertificacionCreateView, CertificacionEditView, ServiciosDeleteView, \
    EquipoDeleteView, CertificacionDeleteView, ContactonDeleteView, ListarUsuarios, crear_usuario_ajax, \
    update_usuario_ajax, DetalleUsuarioView, ClientesDeleteView, ListarInformesView, InformeEditView, \
    InformeCreateView, ListarInformesClienteView, login_success, get_filter_options, get_informe_chart, informe_per_category_chart

app_name = 'panel'

urlpatterns = [

    path('login_success/', login_success, name='login_success'),

    path('solicitudes/', PanelView, name="listar-solicitudes"),
    path('solicitud/<int:id>', DetalleReclamoView, name="detalle-reclamo"),
    path('solicitud/nuevo/', EnviarReclamoView, name="crear-reclamo"),
    path('form/form_ajax', form_enviar_reclamo_ajax, name='form-reclamo--ajax'),
    path('form/reclamo/form_ajax/<int:id>/', update_reclamo_ajax, name='form-update-reclamo-ajax'),
    path('form/respuesta/form_ajax/', respuesta_reclamo_ajax, name='form-respuesta-reclamo-ajax'),

    path('', ListarInformesView, name='panel'),
    path('my/informes/', ListarInformesClienteView, name="listar-informes-clientes"),
    path('informe/<int:id>', InformeEditView, name="editar-informe"),
    path('informe/nuevo/', InformeCreateView, name="crear-informe"),

    path('usuarios/', ListarUsuarios, name="listar-usuarios"),
    path('usuarios/nuevo/form_ajax/', crear_usuario_ajax, name="form-crear-usuario-por-ajax"),
    path('usuario/<int:id>', DetalleUsuarioView, name="detalle-usuario"),
    path('usuarios/editar/form_ajax/<int:id>/', update_usuario_ajax, name='form-update-usuario-ajax'),
    # path('usuarios/eliminar/<int:id>', UsuariosDeleteView, name="eliminar-usuario"),

    path('clientes/', ListarClientesView, name="listar-cliente"),
    path('cliente/<int:id>', DetalleClienteView, name="detalle-cliente"),
    path('cliente/nuevo/form_ajax/', crear_cliente_ajax, name='form-nuevo-cliente'),
    path('cliente/editar/form_ajax/<int:id>/', update_cliente_ajax, name='form-update-cliente-ajax'),
    path('cliente/eliminar/<int:id>/', ClientesDeleteView, name='eliminar-cliente'),

    path('modulo/contactos/', ContactoPanelView, name="listar-contactos"),
    path('modulo/contactos/eliminar/<int:id>', ContactonDeleteView, name="eliminar-contacto"),

    path('modulo/servcios/', ServiciosPanelView, name="listar-servicios"),
    path('modulo/servicio/<int:id>', ServiciosEditarView, name="detalle-servicio"),
    path('modulo/servicio/eliminar/<int:id>', ServiciosDeleteView, name="eliminar-servicio"),
    path('modulo/servicio/nuevo/', ServicioCrearView, name="crear-servicio"),

    path('modulo/equipo/', EquipoListView, name="listar-equipo"),
    path('modulo/equipo/nuevo/', EquipoCreateView, name="crear-equipo"),
    path('modulo/equipo/<int:id>', EquipoEditView, name="editar-equipo"),
    path('modulo/equipo/eliminar/<int:id>', EquipoDeleteView, name="eliminar-equipo"),

    path('modulo/certificaciones/', CertificacionListView, name="listar-certificacion"),
    path('modulo/certificaciones/nuevo/', CertificacionCreateView, name="crear-certificacion"),
    path('modulo/certificacion/<int:id>', CertificacionEditView, name="editar-certificacion"),
    path('modulo/certificacion/eliminar/<int:id>', CertificacionDeleteView, name="eliminar-certificado"),

    path('salir/', LogoutView, name="salir"),

    #url chart
    path('chart/filter-options/', get_filter_options, name='chart-filter-options'),
    path('chart/informes/<int:year>/', get_informe_chart, name='chart-informes'),
    path('chart/informes/tipo/<int:year>/', informe_per_category_chart, name='chart-informe-tipo'),
]
