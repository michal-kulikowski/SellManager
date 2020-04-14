import os

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField

from core.models import Dom, Typ, Symbole, Lokale, Konkurencja, ProbyKontaktu


class DateInput(forms.DateInput):
    input_type = 'date'


class EditDomForm(forms.ModelForm):
    class Meta:
        model = Dom
        fields = ('licz_lokali', 'predkosc_max',)

        licz_lokali = forms.FloatField(label='Liczba lokali', required=False)
        predkosc_max = forms.FloatField(label='Prędkość MAX', required=False)


class EditTypBudynekForm(forms.ModelForm):
    class Meta:
        model = Typ
        fields = ('nazwa_typu',)


class EditSymbolForm(forms.ModelForm):
    class Meta:
        model = Symbole
        fields = ('symbol',)

        symbol = forms.CharField(required=False)


class LokalForm(forms.ModelForm):
    class Meta:
        model = Lokale
        fields = (
            'numer_mieszkania', 'nasz_klient', 'konkurencji_klient', 'data_kontaktu', 'data_konca_umowy', 'data_kolejnego_kontaktu', 'konkurencja', 'klatka', 'opis', 'price', 'imie_klienta', 'telefon')

        widgets = {
            'data_kontaktu': DateInput(attrs={'type': 'date'}),
            'data_konca_umowy': DateInput(attrs={'type': 'date'}),
        }

    klatka = forms.CharField(required=False)
    opis = forms.CharField(required=False)
    imie_klienta = forms.CharField(required=False)
    telefon = forms.IntegerField(required=False, label='Telefon kontaktowy')
    price = forms.FloatField(required=False, label='Obecnie płaci')
    konkurencja = forms.ModelChoiceField(queryset=Konkurencja.objects.all(), required=False)
    data_kolejnego_kontaktu = forms.DateField(initial=None, required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_kontaktu = forms.DateField(initial=None, required=True,  widget=forms.DateInput(attrs={'type': 'date'}))


class ProbaForm(forms.ModelForm):
    class Meta:
        model = ProbyKontaktu
        fields = (
            'numer_mieszkania',)


class FileFieldForm(forms.Form):
    ilosc = forms.IntegerField(required=True, label='Ilość')
    opis = forms.CharField(required=False)
    file_field = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'inputfile'}))