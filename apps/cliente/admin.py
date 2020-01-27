from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteModelAdmin(admin.ModelAdmin):
    pass
