from django import forms
from .models import Contacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        exclude = ('fecha',)
        fields = ('nombre_completo', 'email', 'fono', 'mensaje')
