from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.decorators import verified_email_required
from django.template.loader import get_template

from apps.reclamo.models import Reclamo, Respuesta
from apps.reclamo.forms import ReclamoPanelForm
from apps.cliente.models import Cliente

def LogoutView(request):
    logout(request)
    return redirect('/')

@verified_email_required
def PanelView(request):
    data = dict()
    data['mi_reclamo'] = Reclamo.objects.filter(cliente__usuario=request.user)

    return render(request, 'panel.html', data)

def DetalleReclamoView(request, id):
    data = dict()

    detalle_reclamo = Reclamo.objects.get(pk=id)

    data['pk_reclamo'] = id
    data['detalle_reclamo'] = detalle_reclamo
    data['mi_respuesta'] = Respuesta.objects.filter(reclamo_id=id)

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








