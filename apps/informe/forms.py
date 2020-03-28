from django import forms
from .models import Informe

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        exclude = ['fecha_publicacion']
        fields = ['cliente', 'nombre_informe', 'tipo_informe', 'fecha_muestreo', 'fecha_recepcion', 'pdf_file', 'publicado']

