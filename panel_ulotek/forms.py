from core.models import Gminy
from users.models import User

from django import forms


class UlotkiForm(forms.Form):
    osoba = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Ulotkarz'))


class GminyForm(forms.Form):
    gminy = forms.ModelChoiceField(queryset=Gminy.objects.all())
