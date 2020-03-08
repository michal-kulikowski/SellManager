from django.conf.urls import url
from . import views


app_name = 'dashboard'
urlpatterns = [
    url('list', views.list, name='list'),
    url('change-password', views.change_password, name='change_password'),
    url('', views.dashboard, name='dashboard'),
]

