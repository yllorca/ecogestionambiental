import xlwt
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import verified_email_required
from django.template.loader import get_template
from apps.reclamo.models import Reclamo, Respuesta
from apps.reclamo.forms import ReclamoPanelForm, RespuestaPanelForm, EditarReclamoPanelForm
from apps.cliente.models import Cliente
from apps.cliente.forms import CrearClienteForm
from apps.reclamo.filters import ReclamoFilter
from apps.home.models import Contacto, Servcio, Equipo, Certificacion
from apps.home.forms import ServicioForm, EquipoForm

def LogoutView(request):
    logout(request)
    return redirect('/')

@verified_email_required
def PanelView(request):
    data = dict()

    data['mi_reclamo'] = Reclamo.objects.filter(cliente__usuario=request.user)

    reclamos_staff = Reclamo.objects.all().order_by('id')

    data['reclamos_staff'] = reclamos_staff

    reclamos_filter = ReclamoFilter(request.GET, queryset=reclamos_staff)

    data['filter'] = reclamos_filter

    if request.method == 'GET' and 'accion_requerida' in request.GET:

        if request.GET['accion_requerida'] == 'exportar_datos':

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="reclamos.xls"'
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Registros')

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Fecha', 'Tipo de Solicitud', 'Categoría', 'Cliente', 'Estado']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for registro in reclamos_filter.qs:
                row_num += 1
                ws.write(row_num, 0, '{}/{}/{}'.format(registro.fecha_ingreso.day, registro.fecha_ingreso.month,
                                                       registro.fecha_ingreso.year), font_style)
                ws.write(row_num, 1, registro.get_tipo_solicitud_display(), font_style)
                ws.write(row_num, 2, registro.get_categoria_display(), font_style)
                ws.write(row_num, 3, registro.cliente.razon_social, font_style)
                ws.write(row_num, 4, registro.get_estado_display(), font_style)

            wb.save(response)
            return response

    return render(request, 'panel.html', data)

def DetalleReclamoView(request, id):
    data = dict()

    detalle_reclamo = Reclamo.objects.get(pk=id)

    data['form_reclamo'] = EditarReclamoPanelForm(instance=detalle_reclamo)

    data['pk_reclamo'] = id
    data['detalle_reclamo'] = detalle_reclamo
    data['mi_respuesta'] = Respuesta.objects.filter(reclamo_id=id)

    form_respuesta = RespuestaPanelForm()
    form_respuesta.fields['reclamo'].initial = id
    form_respuesta.fields['usuario_interno'].initial = request.user

    data['form_respuesta'] = form_respuesta

    return render(request, 'panel-detalle-reclamo.html', data)

def EnviarReclamoView(request):

    data = dict()

    mi_cliente = Cliente.objects.get(usuario=request.user)

    form = ReclamoPanelForm()
    form.fields['estado'].initial = 1
    form.fields['cliente'].initial = mi_cliente.id

    data['form'] = form
    data['mi_cliente'] = mi_cliente

    return render(request, 'crear-reclamo.html', data)

def form_enviar_reclamo_ajax(request):
    """
    Funcion que valida un formulario mediante ajax
    :param request: request.POST
    :return : Json
    """
    data = dict()

    mi_cliente = Cliente.objects.get(usuario=request.user)

    if request.method == 'POST':
        form = ReclamoPanelForm(request.POST)
        if form.is_valid():
            # respuesta para el js
            data['respuesta'] = 'ok'

            # guardo la informacion de la solicitud
            form.save()

            # obtengo la informacion
            cliente = request.POST['cliente']
            tipo_solicitud = request.POST['tipo_solicitud']
            estado = request.POST['estado']
            categoria = request.POST['categoria']
            texto = request.POST['texto']

            template = get_template('email/detalle-email-reclamo.html')

            # buscar el label de la sede
            label_tipo_solicitud = ''
            for x in Reclamo.TIPO_SOLICITUD:
                if x[0] == tipo_solicitud:
                    label_tipo_solicitud = x[1]

            # buscar el label de la tipo_discapacidad
            label_estado = ''
            for x in Reclamo.ESTADO:
                if x[0] == estado:
                    label_estado = x[1]

            label_categoria = ''
            for x in Reclamo.CAT:
                if x[0] == categoria:
                    label_categoria = x[1]

            ctx = {
                'cliente': mi_cliente.razon_social,
                'tipo_solicitud': label_tipo_solicitud,
                'estado': label_estado,
                'categoria': label_categoria,
                'texto': texto,

            }
            contenido = template.render(ctx)

            msg = EmailMultiAlternatives(
                'Contacto Alumni IPVG',
                contenido,
                'noresponder@virginiogomez.cl',
                ['yllorca@helloworld.cl'],
            )
            msg.attach_alternative(contenido, "text/html")

            msg.send()
        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'

    return JsonResponse(data)

def update_reclamo_ajax(request, id):
    data = dict()

    detalle_reclamo = Reclamo.objects.get(pk=id)

    if request.method == 'POST':
        form_reclamo = EditarReclamoPanelForm(request.POST, instance=detalle_reclamo)
        if form_reclamo.is_valid():
            data['respuesta'] = 'ok'
            form_reclamo.save()
        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form_reclamo.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'
        data['form_reclamo'] = EditarReclamoPanelForm(request.POST, instance=detalle_reclamo)

    return JsonResponse(data)

def respuesta_reclamo_ajax(request):
    data = dict()

    if request.method == 'POST':
        form_respuesta = RespuestaPanelForm(request.POST)
        if form_respuesta.is_valid():
            data['respuesta'] = 'ok'
            form_respuesta.save()
        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form_respuesta.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'
        data['form_respuesta'] = RespuestaPanelForm()

    return JsonResponse(data)

def ListarClientesView(request):
    data = dict()
    form_cliente = CrearClienteForm()

    data['clientes'] = Cliente.objects.all()
    data['form_cliente'] = form_cliente

    return render(request, 'clientes.html', data)

def crear_cliente_ajax(request):
    data = dict()

    if request.method == 'POST':
        form_cliente = CrearClienteForm(request.POST)
        if form_cliente.is_valid():
            data['respuesta'] = 'ok'
            form_cliente.save()
        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form_cliente.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'
        data['form_cliente'] = CrearClienteForm()

    return JsonResponse(data)

def DetalleClienteView(request, id):
    data = dict()

    detalle_cliente = Cliente.objects.get(pk=id)

    data['form_cliente'] = CrearClienteForm(instance=detalle_cliente)

    data['pk_cliente'] = id
    data['detalle_cliente'] = detalle_cliente

    return render(request, 'panel-detalle-cliente.html', data)

def update_cliente_ajax(request, id):
    data = dict()

    detalle_cliente = Cliente.objects.get(pk=id)

    if request.method == 'POST':
        form_cliente = CrearClienteForm(request.POST, instance=detalle_cliente)
        if form_cliente.is_valid():
            data['respuesta'] = 'ok'
            form_cliente.save()
        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form_cliente.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'
        data['form_cliente'] = CrearClienteForm(request.POST, instance=detalle_cliente)

    return JsonResponse(data)

def ContactoPanelView(request):
    data = dict()
    data['contactos'] = Contacto.objects.all().order_by('-id')

    return render(request, 'panel-contactos.html', data)

def ServiciosPanelView(request):
    data = dict()
    data['servicios'] = Servcio.objects.all().order_by('-id')

    return render(request, 'panel-servicios.html', data)

def ServiciosEditarView(request, id=None):
    data = dict()

    detalle_servicio = Servcio.objects.get(pk=id)

    form_servicio = ServicioForm(request.POST or None, request.FILES or None, instance=detalle_servicio)

    if form_servicio.is_valid():
        update_servicio = form_servicio.save()

        if 'img' in request.FILES:
            update_servicio.img = request.FILES['img']
            update_servicio.save()

        return redirect("panel:listar-servicios")

    data['detalle_servicio'] = detalle_servicio
    data['form_servicio'] = form_servicio

    return render(request, 'panel-detalle-servicio.html', data)

def ServicioCrearView(request):
    data = dict()

    if request.method == 'POST':
        form_servicio = ServicioForm(request.POST)

        if form_servicio.is_valid():
            new_servicio = form_servicio.save()

            ## Guardo la foto una vez creado el servicio, si es que hay foto que agregar
            if 'img' in request.FILES:
                new_servicio.img = request.FILES['img']
                new_servicio.save()

            return redirect('panel:listar-servicios')

    else:
        ## Cre un formulario para crear una noticia
        form_servicio = ServicioForm()

    data['form_servicio'] = form_servicio

    return render(request, 'panel-nuevo-servicio.html', data)

def EquipoListView(request):
    data = dict()
    data['mi_equipo'] = Equipo.objects.all()

    return render(request, 'equipo.html', data)

def EquipoCreateView(request):
    data = dict()

    if request.method == 'POST':
        form_equipo = EquipoForm(request.POST)

        if form_equipo.is_valid():
            new_equipo = form_equipo.save()

            ## Guardo la foto una vez creado
            if 'img' in request.FILES:
                new_equipo.img = request.FILES['img']
                new_equipo.save()

            return redirect('panel:listar-equipo')

    else:
        ## Cre un formulario para crear una noticia
        form_equipo = EquipoForm()

    data['form_equipo'] = form_equipo

    return render(request, 'panel-cerar-equipo.html', data)

def EquipoEditView(request, id=None):
    data = dict()

    detalle_equipo = Equipo.objects.get(pk=id)

    form_equipo = EquipoForm(request.POST or None, request.FILES or None, instance=detalle_equipo)

    if form_equipo.is_valid():
        update_equipo = form_equipo.save()

        if 'img' in request.FILES:
            update_equipo.img = request.FILES['img']
            update_equipo.save()

        return redirect("panel:listar-equipo")

    data['detalle_equipo'] = detalle_equipo
    data['form_equipo'] = form_equipo

    return render(request, 'panel-detalle-equipo.html', data)
#
# def CertificacionListView(request):
#
# def CertificacionCreateView(request):
#
# def CertificacioneditView(request):












