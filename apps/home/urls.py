from django.conf.urls import url
from django.urls import path

from .views import HomeView, form_contacto_ajax, ServicioDetalleView

app_name = 'home'

urlpatterns = [
    path('', HomeView, name='home'),
    path('servicio/<slug:slug>/', ServicioDetalleView, name='detalle-servicio'),
    path('form/form_ajax/', form_contacto_ajax, name='form-contacto-ajax'),
]
