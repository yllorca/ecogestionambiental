from urllib.parse import quote_plus

from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template

from .models import Servcio, Equipo, Certificacion
from .forms import ContactoForm

def HomeView(request):
    data = dict()
    data['servicios'] = Servcio.objects.all().exclude(publicado=False).order_by('id')
    data['integrantes'] = Equipo.objects.all().exclude(publicado=False).order_by('id')
    data['certificaciones'] = Certificacion.objects.all().exclude(publicado=False).order_by('-id')
    data['form'] = ContactoForm()
    return render(request, 'home.html', data)

def ServicioDetalleView(request, slug):
    servicio = get_object_or_404(Servcio, slug=slug)
    if not servicio.publicado:
        raise Http404
    share_string = quote_plus(servicio.nombre)
    ctx = {
        'nombre_servicio': servicio.nombre,
        'servicio': servicio,
        'share_string': share_string,
    }
    return render(request, 'detalle-servicio.html', ctx)

def form_contacto_ajax(request):
    """
    Funcion que valida un formulario mediante ajax
    :param request: request.POST
    :return : Json
    """
    data = dict()

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # respuesta para el js
            data['respuesta'] = 'ok'

            # guardo la informacion de la solicitud
            form.save()

            # obtengo la informacion
            nombre_completo = request.POST['nombre_completo']
            email = request.POST['email']
            fono = request.POST['fono']
            mensaje = request.POST['mensaje']

            template = get_template('email/detalles-email-contacto.html')


            ctx = {
                'nombre_completo': nombre_completo,
                'email': email,
                'fono': fono,
                'mensaje': mensaje,

            }
            contenido = template.render(ctx)

            msg = EmailMultiAlternatives(
                'Contacto Web',
                contenido,
                'noresponder@ecogestionambiental.cl',
                ['jmoscoso@ecogestionambiental.cl', 'aaguilera@ecogestionambiental.cl'],
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


