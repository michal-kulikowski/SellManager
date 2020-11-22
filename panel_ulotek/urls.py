from django.conf.urls import url
from . import views


app_name = 'panel_ulotek'
urlpatterns = [
    url('przypisz-gminy', views.przypisz_gminy, name='przypisz_gminy'),
    url('formularz-gminy', views.formularz_gminy, name='formularz_gminy'),
    url('ulotkowanie', views.ulotkarz, name='ulotkarz'),
    url('', views.base, name='base'),
]

