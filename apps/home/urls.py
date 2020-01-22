from django.conf.urls import url
from .views import HomeView

urlpatterns = [
    url(r'^$', HomeView, name='home')
]
