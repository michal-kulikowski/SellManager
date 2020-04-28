from users.models import User

from django import forms


class UlotkiForm(forms.Form):
    osoba = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Ulotkarz'))
