from typing import List

from django.contrib import admin
from .models import *

@admin.register(Servcio)
class ServicioModelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'publicado')
    list_filter = ('categoria',)

@admin.register(Equipo)
class EquipoModelAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'cargo')
    list_filter = ('cargo',)

@admin.register(Certificacion)
class CertificacionModelAdmin(admin.ModelAdmin):
    list_display = ('nombre_certificacion',)

@admin.register(Contacto)
class ContactoModelAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'fono', 'mensaje')
    date_hierarchy = ('fecha')