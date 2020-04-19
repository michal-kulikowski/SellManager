from django import forms
from tempus_dominus.widgets import DatePicker


class SearchForm(forms.Form):
    handlowiec = forms.CharField(max_length=50, required=False)
    ulica = forms.CharField(max_length=50, required=False)
    miejscowosc = forms.CharField(max_length=50, required=False, label='Miejscowość')
    symbol = forms.CharField(max_length=50, required=False)
    predkosc_od = forms.IntegerField(required=False, label="Prędkość od")
    predkosc_do = forms.IntegerField(required=False, label="Prędkość do")
    hp_od = forms.IntegerField(required=False)
    hp_do = forms.IntegerField(required=False)
    wypelnienie_od = forms.IntegerField(required=False, label="Wypełnienie od")
    wypelnienie_do = forms.IntegerField(required=False, label="Wypełnienie do")
    liczba_klientow_od = forms.IntegerField(required=False, label="Liczba klientów od")
    liczba_klientow_do = forms.IntegerField(required=False, label="Liczba klientów do")
    uruchomienie_od = forms.DateField(required=False, widget=DatePicker(
        options={
            'useCurrent': True,
            'collapse': False,
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ),
    )
    uruchomienie_do = forms.DateField(required=False, widget=DatePicker(
        options={
            'useCurrent': True,
            'collapse': False,
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ),
    )


class DateForm(forms.Form):
    year = forms.DateField(required=False, widget=DatePicker(
        options={
            "format": "YYYY",
            "pickTime": False,
            'useCurrent': True,
            'collapse': False,
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ), label='Rok'
    )
    month = forms.DateField(required=False, widget=DatePicker(
        options={
            "format": "M",
            "pickTime": False,
            'useCurrent': True,
            'collapse': False,
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ), label='Miesiąc'
    )