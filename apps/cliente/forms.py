from django import forms
from django.contrib.auth.models import User

from .models import Cliente

class CrearClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'razon_social', 'direccion', 'fono', 'contacto_comercial', 'usuario']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'is_active')
