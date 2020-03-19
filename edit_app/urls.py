from django.conf.urls import url
from . import views

app_name = 'edit_app'
urlpatterns = [
    url(r'^show_ulotki_redirect/(?P<getIdFromRow>.*)$', views.show_ulotki_photos_redirect, name='show_ulotki_photos_redirect'),
    url('show-ulotki-photos', views.show_ulotki_photos, name='show_ulotki_photos'),
    url(r'^edit_dom_redirect/(?P<getIdFromRow>.*)/(?P<liczba_klientow>.*)$', views.edit_dom_redirect, name='edit_dom_redirect'),
    url(r'^edit_dom_redirect_ulotki/(?P<getIdFromRow>.*)/(?P<liczba_klientow>.*)$', views.edit_dom_redirect_ulotki, name='edit_dom_redirect_ulotki'),
    url(r'^show_lokal_redirect/(?P<getIdFromRow>.*)$', views.show_lokal_redirect, name='show_lokal_redirect'),
    url('edit-dom', views.edit_dom, name='edit_dom'),
    url('show-lokal', views.show_lokal, name='show_lokal'),
    url('rejestracja-zaulotkowania/', views.FileFieldView.as_view(), name='photos_upload'),
    url('dodaj-informacje-klient', views.dodaj_informacje_klient, name='dodaj_informacje_klient'),
    url('dodaj-probe-kontaktu', views.dodaj_probe_kontaktu, name='dodaj_probe_kontaktu'),
]
