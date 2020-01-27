from django.contrib import admin
from .models import Reclamo, Respuesta

@admin.register(Reclamo)
class ReclamoModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Respuesta)
class RespuestaModelAdmin(admin.ModelAdmin):
    pass