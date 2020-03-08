from django.conf.urls import url
from . import views

app_name = 'panel_lokalizacji'
urlpatterns = [
    url('lokalizacje-lista', views.lokalizacje_list, name='lokalizacje_list'),
    url('lokalizacje_json', views.lokalizacje_json, name='lokalizacje_json'),
    url('', views.lokalizacje_list, name='lokalizacje_list'),
]
