from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from itertools import cycle
from django.core.validators import MinLengthValidator, MaxLengthValidator

def validar_rut(rut):
    """
    Función que valida la veracidad del rut del Participante
    :param rut: puede ser ingresado con puntos y guión o sin uno de ellos
    :return: [False]: error en la interfaz | [True] da el visto bueno para la creación
    """
    rut = rut.upper();
    rut = rut.replace("-", "")
    rut = rut.replace(".", "")
    aux = rut[:-1]
    dv = rut[-1:]

    revertido = map(int, reversed(str(aux)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if str(res) == dv:
        pass
    elif dv == "K" and res == 10:
        pass
    else:
        raise ValidationError(_('%(value)s No es un rut válido'), params={'value': rut}, )


class Cliente(models.Model):
    rut = models.CharField(max_length=12, null=False, validators=[validar_rut])
    razon_social = models.CharField(max_length=250)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    fono = models.CharField(max_length=250, blank=True, null=True)
    contacto_comercial = models.CharField(max_length=250, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ["id"]



