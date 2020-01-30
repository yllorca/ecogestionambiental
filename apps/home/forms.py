from django import forms
from .models import Contacto, Servcio, Equipo

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


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        exclude = ('slug',)
        fields = ('nombre_completo', 'cargo', 'url_twitter', 'url_linkedin', 'img', 'publicado')