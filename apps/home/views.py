from django.shortcuts import render
from .models import Servcio, Equipo, Certificacion

def HomeView(request):
    data = dict()
    data['servicios'] = Servcio.objects.all().exclude(publicado=False).order_by('id')
    data['integrantes'] = Equipo.objects.all().exclude(publicado=False).order_by('-id')
    data['certificaciones'] = Certificacion.objects.all().exclude(publicado=False).order_by('-id')
    return render(request, 'home.html', data)

