from django.conf.urls import url
from . import views

app_name = 'raporty'
urlpatterns = [
    url('zdjecie-instalacji/', views.zdjecia_instalacja, name='zdjecia_instalacja'),
    url(r'^zdjecie-instalacji-redirect/(?P<getIdFromRow>.*)$', views.zdjecia_instalacja_redirect,
        name='zdjecia_instalacja_redirect'),
    url('zdjecie-ulotek/', views.zdjecia_ulotek, name='zdjecia_ulotek'),
    url(r'^zdjecie-ulotek-redirect/(?P<getIdFromRow>.*)$', views.zdjecia_ulotek_redirect,
        name='zdjecia_ulotek_redirect'),
    url('instalacje', views.raport_instalacje, name='raport_instalacje'),
    url('ulotki', views.raport_ulotki, name='raport_ulotki'),
    url('', views.raporty, name='raporty'),
]
