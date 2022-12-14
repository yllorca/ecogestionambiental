import xlwt
import pytz
from django.contrib.auth import logout
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import verified_email_required
from django.template.loader import get_template

from apps.informe.models import Informe
from apps.informe.forms import InformeForm
from apps.informe.filter import InformeFilter
from apps.panel.utils import get_year_dict, months, colorPrimary, generate_color_palette
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

def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_staff:
        # user is an admin
        return redirect("panel:panel")
    else:
        return redirect("panel:listar-informes-clientes")

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

            columns = ['Fecha', 'Tipo de Solicitud', 'Categor??a', 'Cliente', 'Estado']

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

    correo_segun_solicitud = {'1': 'aaguilera@ecogestionambiental.cl',
                              '2': 'aaguilera@ecogestionambiental.cl',
                              '3': 'laboratorio@ecogestionambiental.cl'}

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
                'Nuevo ingreso de solicitud',
                contenido1,
                'noresponder@ecogestionambiental.cl',
                [correo_segun_solicitud[str(tipo_solicitud)],'admin@ecogestionambiental.cl', 'jmoscoso@ecogestionambiental.cl'],
            )
            msg1.attach_alternative(contenido1, "text/html")

            msg1.send()

            msg2 = EmailMultiAlternatives(
                'Nuevo ingreso de solicitud',
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()
        form_cliente = CrearClienteForm()
        # form_user = UserForm()

        data['clientes'] = Cliente.objects.all()
        data['form_cliente'] = form_cliente
        # data['form_user'] = form_user

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Cliente creado con ??xito'
            del request.session['creado']

        # # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        # if 'editado' in request.session:
        #     data['editado'] = 'Usuario editado con ??xito'
        #     del request.session['creado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'eliminado' in request.session:
            data['eliminado'] = 'Cliente y usuario eliminados con ??xito'
            del request.session['eliminado']

        return render(request, 'clientes.html', data)
    raise Http404

@verified_email_required
def crear_cliente_ajax(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()

        detalle_cliente = Cliente.objects.get(pk=id)

        data['form_cliente'] = CrearClienteForm(instance=detalle_cliente)

        data['pk_cliente'] = id
        data['detalle_cliente'] = detalle_cliente

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Cliente editado con ??xito'
            del request.session['editado']

        return render(request, 'panel-detalle-cliente.html', data)
    raise Http404

@verified_email_required
def update_cliente_ajax(request, id):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        cliente = get_object_or_404(User, pk=id)
        cliente.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-cliente")
    raise Http404

@verified_email_required
def ListarUsuarios(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()
        form_usuario = UsuarioForm()

        data['usuarios'] = User.objects.all().exclude(is_superuser=True)
        data['form_usuario'] = form_usuario

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Usuario creado con ??xito'
            del request.session['creado']

        # # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        # if 'editado' in request.session:
        #     data['editado'] = 'Usuario editado con ??xito'
        #     del request.session['creado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'eliminado' in request.session:
            data['eliminado'] = 'Usuario y Cliente eliminados'
            del request.session['eliminado']

        return render(request, 'usuarios.html', data)
    raise Http404

@verified_email_required
def crear_usuario_ajax(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()

        detalle_usuario = User.objects.get(pk=id)

        data['form_usuario'] = UsuarioForm(instance=detalle_usuario)

        data['pk_usuario'] = id
        data['detalle_usuario'] = detalle_usuario

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Usuario editado con ??xito'
            del request.session['editado']

        return render(request, 'panel-detalle-usuario.html', data)
    raise Http404

@verified_email_required
def update_usuario_ajax(request, id):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()

        data['servicios'] = Servcio.objects.all().order_by('-id')

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con ??xito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con ??xito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con ??xito'
            del request.session['eliminado']

        return render(request, 'panel-servicios.html', data)
    raise Http404

@verified_email_required
def ServiciosEditarView(request, id=None):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        servicio = get_object_or_404(Servcio, pk=id)
        servicio.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-servicios")
    raise Http404

@verified_email_required
def ServicioCrearView(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()
        data['mi_equipo'] = Equipo.objects.all()

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con ??xito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con ??xito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con ??xito'
            del request.session['eliminado']

        return render(request, 'equipo.html', data)
    raise Http404

@verified_email_required
def EquipoCreateView(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        equipo = get_object_or_404(Equipo, pk=id)
        equipo.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-equipo")
    raise Http404

@verified_email_required
def EquipoEditView(request, id=None):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        data = dict()
        data['mis_certificados'] = Certificacion.objects.all()

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Objeto editado con ??xito'
            del request.session['editado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Objeto creado con ??xito'
            del request.session['creado']

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con ??xito'
            del request.session['eliminado']

        return render(request, 'certificaciones.html', data)
    raise Http404

@verified_email_required
def CertificacionCreateView(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
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
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        certificado = get_object_or_404(Certificacion, pk=id)
        certificado.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-certificacion")
    raise Http404

@verified_email_required
def ContactoPanelView(request):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:

        data = dict()
        data['contactos'] = Contacto.objects.all().order_by('-id')

        if 'eliminado' in request.session:
            data['eliminado'] = 'Objeto eliminado con ??xito'
            del request.session['eliminado']

        return render(request, 'panel-contactos.html', data)
    raise Http404

@verified_email_required
def ContactonDeleteView(request, id):
    users_in_group = Group.objects.get(name="admin").user_set.all()
    if request.user in users_in_group:
        contacto = get_object_or_404(Contacto, pk=id)
        contacto.delete()
        # variable de session usada para notificar que salio todo bien
        request.session['eliminado'] = True
        return redirect("panel:listar-contactos")
    raise Http404

@verified_email_required
def ListarInformesView(request):
    tz = pytz.timezone("America/Santiago")

    if request.user.is_staff:
        data = dict()
        form_informe = InformeForm()

        informes = Informe.objects.all().order_by('-id')

        data['form_informe'] = form_informe
        data['informes'] = informes

        informe_filter = InformeFilter(request.GET, queryset=informes)

        data['filter'] = informe_filter

        if request.method == 'GET' and 'accion_requerida' in request.GET:

            if request.GET['accion_requerida'] == 'exportar_datos':

                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="informes.xls"'
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet('Registros')

                # Sheet header, first row
                row_num = 0

                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                columns = ['N??', 'Cliente', 'Nombre del Informe', 'Tipo de Informe', 'Fecha Muestreo', 'fecha_recepcion', 'Fecha Publicaci??n', 'Fecha de Actualizaci??n']

                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], font_style)

                # Sheet body, remaining rows
                font_style = xlwt.XFStyle()

                for registro in informe_filter.qs:
                    row_num += 1
                    ws.write(row_num, 0, registro.pk ,font_style)
                    ws.write(row_num, 1, registro.cliente.razon_social, font_style)
                    ws.write(row_num, 2, registro.nombre_informe, font_style)
                    ws.write(row_num, 3, registro.get_tipo_informe_display(), font_style)
                    ws.write(row_num, 4, registro.fecha_muestreo, font_style)
                    ws.write(row_num, 5, registro.fecha_recepcion, font_style)
                    ws.write(row_num, 6, registro.fecha_publicacion.astimezone(tz).strftime("%Y/%m/%d %H:%M"), font_style)
                    ws.write(row_num, 7, registro.updated_at.astimezone(tz).strftime("%Y/%m/%d %H:%M"), font_style)

                wb.save(response)
                return response

        # # # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'creado' in request.session:
            data['creado'] = 'Informe creado con ??xito'
            del request.session['creado']

        # Verifico si esta la variable de sesion producto de un redireccionamiento de otra funcion
        if 'editado' in request.session:
            data['editado'] = 'Informe editado con ??xito'
            del request.session['editado']

        return render(request, 'informes.html', data)

    raise Http404

@verified_email_required
def InformeCreateView(request):
    if request.user.is_staff:
        data = dict()

        if request.method == 'POST':
            form_informe = InformeForm(request.POST)

            if form_informe.is_valid():
                new_informe = form_informe.save()

                ## Guardo la foto una vez creado
                if 'pdf_file' in request.FILES:
                    new_informe.pdf_file = request.FILES['pdf_file']
                    new_informe.save()

                # variable de session usada para notificar que salio todo bien
                request.session['creado'] = True

                # obtengo la informacion
                cliente = request.POST['cliente']
                nombre_informe = request.POST['nombre_informe']
                tipo_informe = request.POST['tipo_informe']
                fecha_muestreo = request.POST['fecha_muestreo']
                fecha_recepcion = request.POST['fecha_recepcion']

                # obtengo la informacion
                template1 = get_template('email/notifica-informe.html')

                # buscar el label de la tipo de informe
                label_tipo_informe = ''
                for x in Informe.TIPO_INFORME:
                    if x[0] == tipo_informe:
                        label_tipo_informe = x[1]

                ctx = {
                    'cliente': cliente,
                    'nombre_informe': nombre_informe,
                    'tipo_informe': label_tipo_informe,
                    'fecha_muestreo': fecha_muestreo,
                    'fecha_recepcion': fecha_recepcion,
                }

                contenido1 = template1.render(ctx)

                msg1 = EmailMultiAlternatives(
                    'Nuevo informe disponible',
                    contenido1,
                    'noresponder@ecogestionambiental.cl',
                    [new_informe.cliente.usuario.email],
                )
                msg1.attach_alternative(contenido1, "text/html")

                msg1.send()

                return redirect('panel:panel')

            else:
                data['respuesta'] = 'error'
                mensaje_error = '<strong>Campos:</strong> <br><ul>'
                for e in form_informe.errors:
                    mensaje_error = '{}<li>{}</li>'.format(mensaje_error, e)
                data['mensaje'] = '{}{}'.format(mensaje_error, '</ul>')

        else:
            ## Cree un formulario para crear una noticia
            form_informe = InformeForm()

        data['form_informe'] = form_informe

        return render(request, 'panel-crear-informe.html', data)
    raise Http404

@verified_email_required
def InformeEditView(request, id=None):
    if request.user.is_staff:
        data = dict()

        detalle_informe = Informe.objects.get(pk=id)

        form_informe = InformeForm(request.POST or None, request.FILES or None, instance=detalle_informe)

        if form_informe.is_valid():
            update_informe = form_informe.save()

            if 'pdf_file' in request.FILES:
                update_informe.pdf_file = request.FILES['pdf_file']
                update_informe.save()

            # variable de session usada para notificar que salio todo bien
            request.session['editado'] = True

            return redirect("panel:panel")

        else:
            data['respuesta'] = 'error'
            mensaje_error = '<strong>Campos:</strong> <br><ul>'
            for e in form_informe.errors:
                mensaje_error = '{}<li>{}</li>'.format(mensaje_error, e)
            data['mensaje'] = '{}{}'.format(mensaje_error, '</ul>')

        data['detalle_informe'] = detalle_informe
        data['form_informe'] = form_informe

        return render(request, 'panel-detalle-informe.html', data)
    raise Http404

@verified_email_required
def ListarInformesClienteView(request):
    data = dict()

    data['mis_informes'] = Informe.objects.filter(cliente__usuario=request.user).order_by('-id').exclude(publicado=False)

    return render(request, 'informes.html', data)

def get_filter_options(request):
    grouped_courses = Informe.objects.filter(publicado=True).annotate(year=ExtractYear('fecha_publicacion')).values('year').order_by('-year').distinct()
    options = [course['year'] for course in grouped_courses]

    return JsonResponse({
        'options': options,
    })

def get_informe_chart(request, year):
    informes = Informe.objects.filter(publicado=True, fecha_publicacion__year=year)
    grouped_courses = informes.annotate(month=ExtractMonth('fecha_publicacion')) \
        .values('month').annotate(informe_count=Count('id')).values('month', 'informe_count').order_by('month')

    informes_dict = get_year_dict()

    for group in grouped_courses:
        informes_dict[months[group['month']-1]] = round(group['informe_count'], 2)

    return JsonResponse({
        'title': f'A??o: {year}',
        'data': {
            'labels': list(informes_dict.keys()),
            'datasets': [{
                'label': 'Cantidad de Informes por mes',
                'backgroundColor': colorPrimary,
                'borderColor': colorPrimary,
                'data': list(informes_dict.values()),
            }]
        },
    })

def informe_per_category_chart(request, year):

    informes = Informe.objects.filter(publicado=True, fecha_publicacion__year=year)
    grouped_informe = informes.values('tipo_informe').annotate(tipo_informe_count=Count('id')).values('tipo_informe', 'tipo_informe_count')

    tipo_informe_dict = dict()

    for tipo_informe in Informe.TIPO_INFORME:
        tipo_informe_dict[tipo_informe[1]] = 0

    for group in grouped_informe:
        tipo_informe_dict[dict(Informe.TIPO_INFORME)[group['tipo_informe']]] = group['tipo_informe_count']

    return JsonResponse({
        'title': f'A??o: {year}',
        'data': {
            'labels': list(tipo_informe_dict.keys()),
            'datasets': [{
                'label': 'Total Cursos',
                'backgroundColor': generate_color_palette(len(tipo_informe_dict)),
                'borderColor': generate_color_palette(len(tipo_informe_dict)),
                'data': list(tipo_informe_dict.values()),
            }]
        },
    })
