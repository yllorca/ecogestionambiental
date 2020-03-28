import django_filters
from apps.informe.models import Informe

class InformeFilter(django_filters.FilterSet):
    # fecha_publicacion = django_filters.NumberFilter(field_name='fecha_publicacion', lookup_expr='year', label='Fecha Publicación (Año)')
    # fecha_publicacion__month = django_filters.NumberFilter(field_name='fecha_publicacion', lookup_expr='month', label='Fecha Publicación (Mes)')
    class Meta:
        model = Informe
        fields = ['cliente', 'tipo_informe', 'publicado']