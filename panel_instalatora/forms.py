import os

from django import forms
from django.core.exceptions import ValidationError

from core.models import Instalacje


class InstalacjaForm(forms.ModelForm):
    class Meta:
        model = Instalacje
        fields = (
            'poprzedni_numer_klienta', 'numer_klienta', 'notatka')

    notatka = forms.CharField(widget=forms.Textarea(attrs={'id': 'text_comments'}), required=False)


class FileFieldFormInstalacje(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'inputfile'}))