from django.contrib import admin
from .models import Informe

# Register your models here.
@admin.register(Informe)
class InformeModelAdmin(admin.ModelAdmin):
    pass