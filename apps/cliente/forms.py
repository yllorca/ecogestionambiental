from django import forms
from .models import Cliente

class CrearClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'razon_social', 'direccion', 'fono', 'contacto_comercial', 'usuario', 'activo']
