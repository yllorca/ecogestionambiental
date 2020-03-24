import xlwt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import verified_email_required
from django.template.loader import get_template
from apps.reclamo.models import Reclamo, Respuesta
from apps.reclamo.forms import ReclamoPanelForm, RespuestaPanelForm, EditarReclamoPanelForm
from apps.cliente.models import Cliente
from apps.cliente.forms import CrearClienteForm, UsuarioForm
from apps.reclamo.filters import ReclamoFilter
from apps.home.models import Contacto, Servcio, Equipo, Certificacion
from apps.home.forms import ServicioForm, EquipoForm, CertificadoForm

def LogoutView(request):
    logout(request)
    return redirect('/')

@verified_email_required
def PanelView(request):
    data = dict()

    data['mi_reclamo'] = Reclamo.objects.filter(cliente__usuario=request.user).order_by('-id')

    reclamos_staff = Reclamo.objects.all().order_by('-id')

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

@verified_email_required
def DetalleReclamoView(request, id):
    data = dict()

    detalle_reclamo = Reclamo.objects.get(pk=id)

    if request.user.id == detalle_reclamo.cliente.usuario.id or request.user.is_staff:

        data['form_reclamo'] = EditarReclamoPanelForm(instance=detalle_reclamo)

        data['pk_reclamo'] = id

        data['detalle_reclamo'] = detalle_reclamo

        data['mi_respuesta'] = Respuesta.objects.filter(reclamo_id=id)

        form_respuesta = RespuestaPanelForm()
        form_respuesta.fields['reclamo'].initial = id
        form_respuesta.fields['usuario_interno'].initial = request.user

        data['form_respuesta'] = form_respuesta

        return render(request, 'panel-detalle-reclamo.html', data)
    else:
        raise Http404

@verified_email_required
def EnviarReclamoView(request):

    data = dict()

    mi_cliente = Cliente.objects.get(usuario=request.user)

    form = ReclamoPanelForm()
    form.fields['estado'].initial = 1
    form.fields['cliente'].initial = mi_cliente.id

    data['form'] = form
    data['mi_cliente'] = mi_cliente

    return render(request, 'crear-reclamo.html', data)

@verified_email_required
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
            tipo_solicitud = request.POST['tipo_solicitud']
            estado = request.POST['estado']
            categoria = request.POST['categoria']
            texto = request.POST['texto']

            template1 = get_template('email/detalle-email-reclamo.html')
            template2 = get_template('email/notificacion-reclamo-cliente.html')


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
                'email': mi_cliente.usuario.email,

            }

            contenido1 = template1.render(ctx)
            contenido2 = template2.render(ctx)

            msg1 = EmailMultiAlternatives(
                'Nuevo Reclamo/Sugerencia',
                contenido1,
                'noresponder@ecogestionambiental.cl',
                ['aaguilera@ecogestionambiental.cl'],
            )
            msg1.attach_alternative(contenido1, "text/html")

            msg1.send()

            msg2 = EmailMultiAlternatives(
                'Nuevo Reclamo/Sugerencia',
                contenido2,
                'noresponder@ecogestionambiental.cl',
                [mi_cliente.usuario.email],
            )
            msg2.attach_alternative(contenido2, "text/html")

            msg2.send()

        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos requeridos:</strong> <br>'
            for e in form.errors:
                mensaje_error = mensaje_error + ' [{}] '.format(e)
            data['mensaje'] = mensaje_error
    else:
        data['respuesta'] = 'error'

    return JsonResponse(data)

@verified_email_required
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

@verified_email_required
def respuesta_reclamo_ajax(request):
    data = dict()

    # respuesta = Respuesta.objects.get(reclamo_id=id)

    if request.method == 'POST':
        form_respuesta = RespuestaPanelForm(request.POST)
        if form_respuesta.is_valid():
            data['respuesta'] = 'ok'
            respuesta_new = form_respuesta.save()

            # obtengo la informacion
            template1 = get_template('email/respuesta-reclamo.html')

            # buscar el label de la tipo_discapacidad

            label_estado = ''
            for x in Reclamo.ESTADO:
                if x[0] == respuesta_new.reclamo.estado:
                    label_estado = x[1]

            ctx = {
                'detalle_respuesta': respuesta_new.detalle_respuesta,
                'fecha_respuesta': respuesta_new.fecha_respuesta,
                'reclamo_id': respuesta_new.reclamo.pk,
                'reclamo_estado': label_estado,
                'cliente': respuesta_new.reclamo.cliente.razon_social
            }

            contenido1 = template1.render(ctx)

            msg1 = EmailMultiAlternatives(
                'Respuesta a requerimento',
                contenido1,
                'noresponder@ecogestionambiental.cl',
                [respuesta_new.reclamo.cliente.usuario.email],
            )
            msg1.attach_alternative(contenido1, "text/html")

            msg1.send()


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

@verified_email_required
def ListarClientesView(request):
    if request.user.is_staff:
        data = dict()
        form_cliente = CrearClienteForm()
        # form_user = UserForm()

        data['clientes'] = Cliente.objects.all()
        data['form_cliente'] = form_cliente
        # data['form_user'] = form_user

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Cliente creado con éxito'
            del request.session['creado']

        # # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        # if 'editado' in request.session:
        #     data['editado'] = 'Usuario editado con éxito'
        #     del request.session['creado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'eliminado' in request.session:
            data['eliminado'] = 'Cliente y usuario eliminados con éxito'
            del request.session['eliminado']

        return render(request, 'clientes.html', data)
    raise Http404

@verified_email_required
def crear_cliente_ajax(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_cliente = CrearClienteForm(request.POST)

            if form_cliente.is_valid():
                data['respuesta'] = 'ok'
                form_cliente.save()
                request.session['creado'] = True
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
    raise Http404

@verified_email_required
def DetalleClienteView(request, id):
    if request.user.is_staff:
        data = dict()

        detalle_cliente = Cliente.objects.get(pk=id)

        data['form_cliente'] = CrearClienteForm(instance=detalle_cliente)

        data['pk_cliente'] = id
        data['detalle_cliente'] = detalle_cliente

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Cliente editado con éxito'
            del request.session['editado']

        return render(request, 'panel-detalle-cliente.html', data)
    raise Http404

@verified_email_required
def update_cliente_ajax(request, id):
    if request.user.is_staff:
        data = dict()

        detalle_cliente = Cliente.objects.get(pk=id)

        if request.method == 'POST':
            form_cliente = CrearClienteForm(request.POST, instance=detalle_cliente)
            if form_cliente.is_valid():
                data['respuesta'] = 'ok'
                form_cliente.save()
                request.session['editado'] = True
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
    raise Http404

@verified_email_required
def ClientesDeleteView(request, id):
    if request.user.is_staff:
        cliente = get_object_or_404(User, pk=id)
        cliente.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-cliente")
    raise Http404

@verified_email_required
def ListarUsuarios(request):
    if request.user.is_staff:
        data = dict()
        form_usuario = UsuarioForm()

        data['usuarios'] = User.objects.all().exclude(is_superuser=True)
        data['form_usuario'] = form_usuario

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Usuario creado con éxito'
            del request.session['creado']

        # # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        # if 'editado' in request.session:
        #     data['editado'] = 'Usuario editado con éxito'
        #     del request.session['creado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'eliminado' in request.session:
            data['eliminado'] = 'Usuario y Cliente eliminados'
            del request.session['eliminado']

        return render(request, 'usuarios.html', data)
    raise Http404

@verified_email_required
def crear_usuario_ajax(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_usuario = UsuarioForm(request.POST)

            if form_usuario.is_valid():
                data['respuesta'] = 'ok'
                form_usuario.save()

                # variable de session usada para notificar que salio todo bien
                request.session['creado'] = True

            else:
                data['respuesta'] = 'error'
                mensaje_error = '<strong>Campos:</strong> <br><ul>'
                for e in form_usuario.errors:
                    mensaje_error = '{}<li>{}</li>'.format(mensaje_error, e)
                data['mensaje'] = '{}{}'.format(mensaje_error, '</ul>')

        else:
            ## Cre un formulario para crear una noticia
            data['respuesta'] = 'error'
            data['form_usuario'] = UsuarioForm()

        return JsonResponse(data)
    raise Http404

@verified_email_required
def DetalleUsuarioView(request, id):
    if request.user.is_staff:
        data = dict()

        detalle_usuario = User.objects.get(pk=id)

        data['form_usuario'] = UsuarioForm(instance=detalle_usuario)

        data['pk_usuario'] = id
        data['detalle_usuario'] = detalle_usuario

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Usuario editado con éxito'
            del request.session['editado']

        return render(request, 'panel-detalle-usuario.html', data)
    raise Http404

@verified_email_required
def update_usuario_ajax(request, id):
    if request.user.is_staff:
        data = dict()

        detalle_usuario = User.objects.get(pk=id)

        if request.method == 'POST':
            form_usuario = UsuarioForm(request.POST, instance=detalle_usuario)
            if form_usuario.is_valid():
                data['respuesta'] = 'ok'
                form_usuario.save()
                request.session['editado'] = True
            else:
                data['respuesta'] = 'error'
                mensaje_error = '<strong>Campos:</strong> <br>'
                for e in form_usuario.errors:
                    mensaje_error = mensaje_error + ' [{}] '.format(e)
                data['mensaje'] = mensaje_error
        else:
            data['respuesta'] = 'error'
            data['form_usuario'] = UsuarioForm(request.POST, instance=detalle_usuario)

        return JsonResponse(data)
    raise Http404

# @verified_email_required
# def UsuariosDeleteView(request, id):
#     if request.user.is_staff:
#         usuario = get_object_or_404(User, pk=id)
#         usuario.delete()
#         # variable de session usada para notificar que salio todo bien
#         request.session['eliminado'] = True
#         return redirect("panel:listar-usuarios")
#     raise Http404

@verified_email_required
def ServiciosPanelView(request):
    if request.user.is_staff:
        data = dict()

        data['servicios'] = Servcio.objects.all().order_by('-id')

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con éxito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con éxito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con éxito'
            del request.session['eliminado']

        return render(request, 'panel-servicios.html', data)
    raise Http404

@verified_email_required
def ServiciosEditarView(request, id=None):
    if request.user.is_staff:
        data = dict()

        detalle_servicio = Servcio.objects.get(pk=id)

        form_servicio = ServicioForm(request.POST or None, request.FILES or None, instance=detalle_servicio)

        if form_servicio.is_valid():
            update_servicio = form_servicio.save()

            if 'img' in request.FILES:
                update_servicio.img = request.FILES['img']
                update_servicio.save()

            # variable de session usada para notificar que salio todo bien
            request.session['editado'] = True

            return redirect("panel:listar-servicios")

        data['detalle_servicio'] = detalle_servicio
        data['form_servicio'] = form_servicio

        return render(request, 'panel-detalle-servicio.html', data)
    raise Http404

@verified_email_required
def ServiciosDeleteView(request, id):
    if request.user.is_staff:
        servicio = get_object_or_404(Servcio, pk=id)
        servicio.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-servicios")
    raise Http404

@verified_email_required
def ServicioCrearView(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_servicio = ServicioForm(request.POST)

            if form_servicio.is_valid():
                new_servicio = form_servicio.save()

                ## Guardo la foto una vez creado el servicio, si es que hay foto que agregar
                if 'img' in request.FILES:
                    new_servicio.img = request.FILES['img']
                    new_servicio.save()

                # variable de session usada para notificar que salio todo bien
                request.session['creado'] = True

                return redirect('panel:listar-servicios')

            else:
                mensaje_error = '<strong>Campos requeridos:</strong> <br><ul>'
                for e in form_servicio.errors:
                    mensaje_error = '{}<li>{}</li>'.format(mensaje_error, e)
                data['mensaje'] = '{}{}'.format(mensaje_error, '</ul>')

        else:
            ## Cre un formulario para crear una noticia
            form_servicio = ServicioForm()

        data['form_servicio'] = form_servicio

        return render(request, 'panel-nuevo-servicio.html', data)
    raise Http404

@verified_email_required
def EquipoListView(request):
    if request.user.is_staff:
        data = dict()
        data['mi_equipo'] = Equipo.objects.all()

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con éxito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con éxito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con éxito'
            del request.session['eliminado']

        return render(request, 'equipo.html', data)
    raise Http404

@verified_email_required
def EquipoCreateView(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_equipo = EquipoForm(request.POST)

            if form_equipo.is_valid():
                new_equipo = form_equipo.save()

                ## Guardo la foto una vez creado
                if 'img' in request.FILES:
                    new_equipo.img = request.FILES['img']
                    new_equipo.save()

                request.session['creado'] = True

                return redirect('panel:listar-equipo')

        else:
            ## Cre un formulario para crear una noticia
            form_equipo = EquipoForm()

        data['form_equipo'] = form_equipo

        return render(request, 'panel-cerar-equipo.html', data)
    raise Http404

@verified_email_required
def EquipoDeleteView(request, id):
    if request.user.is_staff:
        equipo = get_object_or_404(Equipo, pk=id)
        equipo.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-equipo")
    raise Http404

@verified_email_required
def EquipoEditView(request, id=None):
    if request.user.is_staff:
        data = dict()

        detalle_equipo = Equipo.objects.get(pk=id)

        form_equipo = EquipoForm(request.POST or None, request.FILES or None, instance=detalle_equipo)

        if form_equipo.is_valid():
            update_equipo = form_equipo.save()

            if 'img' in request.FILES:
                update_equipo.img = request.FILES['img']
                update_equipo.save()

            request.session['editado'] = True

            return redirect("panel:listar-equipo")

        data['detalle_equipo'] = detalle_equipo
        data['form_equipo'] = form_equipo

        return render(request, 'panel-detalle-equipo.html', data)
    raise Http404

@verified_email_required
def CertificacionListView(request):
    if request.user.is_staff:
        data = dict()
        data['mis_certificados'] = Certificacion.objects.all()

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con éxito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con éxito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con éxito'
            del request.session['eliminado']

        return render(request, 'certificaciones.html', data)
    raise Http404

@verified_email_required
def CertificacionCreateView(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_certificado = CertificadoForm(request.POST)

            if form_certificado.is_valid():
                new_certificado = form_certificado.save()

                ## Guardo la foto una vez creado
                if 'img' in request.FILES:
                    new_certificado.img = request.FILES['img']
                    new_certificado.save()

                if 'pdf_file' in request.FILES:
                    new_certificado.pdf_file = request.FILES['pdf_file']
                    new_certificado.save()

                # variable de session usada para notificar que salio todo bien
                request.session['creado'] = True

                return redirect('panel:listar-certificacion')

        else:
            ## Cre un formulario para crear una noticia
            form_certificado = CertificadoForm()

        data['form_certificado'] = form_certificado

        return render(request, 'panel-crear-certificacion.html', data)
    raise Http404

@verified_email_required
def CertificacionEditView(request, id=None):
    if request.user.is_staff:
        data = dict()

        detalle_certificado = Certificacion.objects.get(pk=id)

        form_certificado = CertificadoForm(request.POST or None, request.FILES or None, instance=detalle_certificado)

        if form_certificado.is_valid():
            update_certificado = form_certificado.save()

            if 'img' in request.FILES:
                update_certificado.img = request.FILES['img']
                update_certificado.save()

            # variable de session usada para notificar que salio todo bien
            request.session['editado'] = True

            return redirect("panel:listar-certificacion")

        data['detalle_certificado'] = detalle_certificado
        data['form_certificado'] = form_certificado

        return render(request, 'panel-detalle-certificado.html', data)
    raise Http404

@verified_email_required
def CertificacionDeleteView(request, id):
    if request.user.is_staff:
        certificado = get_object_or_404(Certificacion, pk=id)
        certificado.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-certificacion")
    raise Http404

@verified_email_required
def ContactoPanelView(request):
    if request.user.is_staff:

        data = dict()
        data['contactos'] = Contacto.objects.all().order_by('-id')

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con éxito'
            del request.session['eliminado']

        return render(request, 'panel-contactos.html', data)
    raise Http404

@verified_email_required
def ContactonDeleteView(request, id):
    if request.user.is_staff:
        contacto = get_object_or_404(Contacto, pk=id)
        contacto.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-contactos")
    raise Http404





