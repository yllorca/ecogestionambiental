from django import forms
from .models import Reclamo, Respuesta


class ReclamoPanelForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        exclude = ('fecha_ingreso',)
        fields = ('tipo_solicitud', 'categoria', 'texto', 'cliente', 'estado')

        widgets = {
            'cliente': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
        }

