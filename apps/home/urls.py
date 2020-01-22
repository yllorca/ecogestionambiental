from django.conf.urls import url
from .views import HomeView, form_contacto_ajax

urlpatterns = [
    url(r'^$', HomeView, name='home'),
    url(r'^form/form_ajax$', form_contacto_ajax, name='form-contacto-ajax'),
]
