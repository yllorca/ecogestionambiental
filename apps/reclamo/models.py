from django.db import models
from apps.cliente.models import Cliente
from django.contrib.auth.models import User

class Reclamo(models.Model):
    ESTADO = (
        ('1', 'Abierto'),
        ('2', 'En revisión'),
        ('3', 'Resuelto'),
        ('4', 'Cerrado'),
    )
    TIPO_SOLICITUD = (
        ('1', 'Queja'),
        ('2', 'Sugerencia'),
        ('3', 'Modificación de Informe'),

    )
    CAT = (
        ('1', 'Resultados de Ensayos'),
        ('2', 'Mediciones y muestreos'),
        ('3', 'Atención a clientes'),
        ('4', 'Logística'),
        ('5', 'Cotización'),
        ('6', 'Facturación'),
        ('7', 'Otros'),
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_solicitud = models.CharField(choices=TIPO_SOLICITUD, max_length=25)
    estado = models.CharField(choices=ESTADO, max_length=25)
    categoria = models.CharField(choices=CAT, max_length=25)
    texto = models.TextField(max_length=600)
    fecha_ingreso = models.DateTimeField(auto_now=False, auto_now_add=True)


    def __str__(self):
        return self.cliente.razon_social

    class Meta:
        verbose_name = 'Queja y Segerencia'
        verbose_name_plural = 'Quejas y Sugerencias'
        ordering = ["id"]

class Respuesta(models.Model):
    reclamo = models.ForeignKey(Reclamo, on_delete=models.CASCADE)
    usuario_interno = models.ForeignKey(User, on_delete=models.CASCADE)
    detalle_respuesta = models.TextField(max_length=600)
    fecha_respuesta = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.usuario_interno.username


    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ["id"]






