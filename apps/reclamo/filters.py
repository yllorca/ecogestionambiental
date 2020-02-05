import django_filters
from apps.reclamo.models import Reclamo

class ReclamoFilter(django_filters.FilterSet):
    class Meta:
        model = Reclamo
        fields = ['tipo_solicitud', 'categoria', 'cliente', 'estado', ]