from django.db import models
from apps.cliente.models import Cliente

def upload_location_informe_pdf(instance, filename):
    filebase, extension = filename.split(".")
    return "informes/%s/%s.%s" % (instance.id, instance.id, extension)
    # return "%s/%s" % (instance.id, filename)

# Create your models here.
class Informe(models.Model):
    TIPO_INFORME = (
        ('1', 'Laboratorio de Ensayos'),
        ('2', 'Asesorías'),
        ('3', 'PVA'),
        ('4', 'Aguas Residuales'),
        ('5', 'Muestreo y/o Medición'),
        ('6', 'Aguas Subterráneas'),
        ('7', 'Agua Potable'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre_informe = models.CharField(max_length=250, verbose_name="Nombre del Informe")
    tipo_informe = models.CharField(max_length=250, choices=TIPO_INFORME, verbose_name="Tipo de Informe")
    fecha_muestreo = models.DateField()
    fecha_recepcion = models.DateField()
    pdf_file = models.FileField(upload_to=upload_location_informe_pdf,
                                null=True,
                                blank=True,
                                editable=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)


    def __str__(self):
        return self.nombre_informe

    class Meta:
        verbose_name = 'Informe'
        verbose_name_plural = 'Informes'



