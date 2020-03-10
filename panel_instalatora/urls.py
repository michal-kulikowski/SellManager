from django.conf.urls import url
from . import views

app_name = 'panel_instalatora'
urlpatterns = [
    url('formularz-instalacji', views.formularz_instalacji, name='formularz_instalacji'),
    url('dodanie-zdjec-instalacji/', views.FileFieldView.as_view(), name='dodanie-zdjec-instalacji'),
    url('potwierdzenie-formularza-instalacji/', views.potwierdzenie_formularza_instalacji, name='potwierdzenie_formularza_instalacji'),
    url('podglad-zdjec-z-instalacji/', views.show_photos_instalacja, name='show_photos_instalacja'),
    url(r'^podglad-zdjec-redirect/(?P<getIdFromRow>.*)$', views.show_photos_instalacja_redirect, name='show_photos_instalacja_redirect'),
    url('', views.panel_instalatora, name='panel_instalatora'),
]
