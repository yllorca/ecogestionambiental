from django import forms
from .models import Contacto, Servcio, Equipo, Certificacion

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
        fields = ('nombre_completo', 'cargo', 'url_twitter', 'url_linkedin', 'img', 'publicado')


class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificacion
        fields = ('nombre_certificacion', 'url_referencia', 'img', 'publicado')