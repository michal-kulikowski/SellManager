from django.conf.urls import url
from . import views

app_name = 'edit_app'
urlpatterns = [
    url(r'^show_ulotki_redirect/(?P<getIdFromRow>.*)$', views.show_ulotki_photos_redirect, name='show_ulotki_photos_redirect'),
    url('show-ulotki-photos', views.show_ulotki_photos, name='show_ulotki_photos'),
    url(r'^edit_dom_redirect/(?P<getIdFromRow>.*)$', views.edit_dom_redirect, name='edit_dom_redirect'),
    url(r'^edit_dom_redirect_ulotki/(?P<getIdFromRow>.*)$', views.edit_dom_redirect_ulotki, name='edit_dom_redirect_ulotki'),
    url(r'^show_lokal_redirect/(?P<getIdFromRow>.*)$', views.show_lokal_redirect, name='show_lokal_redirect'),
    url('edit-dom', views.edit_dom, name='edit_dom'),
    url('script', views.script, name='script'),
    url('delete_dom/(?P<getIdFromRow>.*)$', views.delete_dom, name='delete_dom'),
    url('show-lokal', views.show_lokal, name='show_lokal'),
    url('rejestracja-zaulotkowania/', views.FileFieldView.as_view(), name='photos_upload'),
    url('rejestracja-zaulotkowania2/', views.FileFieldView2.as_view(), name='photos_upload2'),
    url('rejestracja_ulotek_redirect/(?P<getIdFromRow>.*)$', views.rejestracja_ulotek_redirect, name='rejestracja_ulotek_redirect'),
    url('dodaj-informacje-klient', views.dodaj_informacje_klient, name='dodaj_informacje_klient'),
    url('rejestracja-konkurencji', views.rejestracja_konkurencji, name='rejestracja_konkurencji'),
    url('dodaj-probe-kontaktu', views.dodaj_probe_kontaktu, name='dodaj_probe_kontaktu'),
]
