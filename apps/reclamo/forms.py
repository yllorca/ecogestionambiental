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


class EditarReclamoPanelForm(forms.ModelForm):
    class Meta:
        model = Reclamo
        exclude = ('fecha_ingreso',)
        fields = ('tipo_solicitud', 'categoria', 'texto', 'cliente', 'estado')

        widgets = {
            'cliente': forms.HiddenInput(),
            'texto': forms.Textarea(attrs={'readonly':'readonly'})
        }

class RespuestaPanelForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        exclude = ('fecha_respuesta',)
        fields = ('detalle_respuesta', 'reclamo', 'usuario_interno', 'reclamo')

        widgets = {
            'reclamo': forms.HiddenInput(),
            'usuario_interno': forms.HiddenInput(),
        }
