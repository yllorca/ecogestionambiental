from django import forms
from .models import Contacto, Servcio

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        exclude = ('fecha',)
        fields = ('nombre_completo', 'email', 'fono', 'mensaje')


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servcio
        exclude = ('slug',)
        fields = ('nombre', 'categoria', 'descripcion', 'img', 'publicado')
