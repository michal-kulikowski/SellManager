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


def my_validate(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    valid = ['.jpg', '.jpeg']
    if ext not in valid:
        raise ValidationError("Nieodpowiedni format, sprawdź czy wgrałeś poprawny plik .jpg")


class FileFieldFormInstalacje(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'inputfile'}), validators=[my_validate])