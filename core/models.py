import datetime
import os
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models

from SellManager import settings


def my_validate(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    valid = ['.jpg', '.jpeg']
    if ext not in valid:
        raise ValidationError("Nieodpowiedni format, sprawdź czy wgrałeś poprawny plik .jpg")


def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=20)
    new_image = File(im_io, name=image.name)
    return new_image


class Sprzedawca(models.Model):
    id_sprzedawca = models.AutoField(primary_key=True)
    nazwa_sprzedawcy = models.CharField(max_length=25, unique=True)


class Kraj(models.Model):
    id_adr_kraj = models.AutoField(primary_key=True)
    nazwa_kraju = models.CharField(max_length=200)


class Wojewodztwo(models.Model):
    id_adr_wojewodztwo = models.AutoField(primary_key=True)
    id_adr_kraj = models.ForeignKey(Kraj, on_delete=models.CASCADE, verbose_name='Kraj', null=True, blank=True)
    nazwa_wojewodztwa = models.CharField(max_length=200)
    nr_terytu = models.CharField(max_length=100)


class Powiat(models.Model):
    id_adr_powiat = models.AutoField(primary_key=True)
    id_adr_wojewodztwo = models.ForeignKey(Wojewodztwo, on_delete=models.CASCADE, verbose_name='Województwo',
                                           null=True, blank=True)
    nazwa_powiatu = models.CharField(max_length=200)
    nazdod = models.CharField(max_length=200)
    nr_terytu = models.CharField(max_length=100)


class Gmina(models.Model):
    id_adr_gmina = models.AutoField(primary_key=True)
    id_adr_powiat = models.ForeignKey(Powiat, on_delete=models.CASCADE, verbose_name='Powiat', null=True, blank=True)
    nazwa_gminy = models.CharField(max_length=200)
    nazdod = models.CharField(max_length=200)
    nr_terytu = models.CharField(max_length=100)


class Miejscowosc(models.Model):
    id_adr_miejscowosc = models.AutoField(primary_key=True)
    id_adr_gmina = models.ForeignKey(Gmina, on_delete=models.CASCADE, verbose_name='Gmina', null=True, blank=True)
    nazwa_miejscowosci = models.CharField(max_length=200)
    nr_terytu = models.CharField(max_length=100)
    nazwa_rm = models.CharField(max_length=100)


class Ulica(models.Model):
    id_adr_ulica = models.AutoField(primary_key=True)
    id_adr_miejscowosc = models.ForeignKey(Miejscowosc, on_delete=models.CASCADE, verbose_name='Miejscowość',
                                           null=True, blank=True)
    typ = models.CharField(max_length=100, null=True)
    nazwa_ulicy_1 = models.CharField(max_length=200, null=True)
    nazwa_ulicy_2 = models.CharField(max_length=200, null=True)
    nazwa_ulicy = models.CharField(max_length=200, null=True)
    nr_terytu = models.CharField(max_length=100, null=True)


class Technologie(models.Model):
    id_gniazdka_technologie = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=20)


class Konkurencja(models.Model):
    nazwa_konkurencji = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.nazwa_konkurencji


class Dom(models.Model):
    id_adr_dom = models.AutoField(primary_key=True)
    numer_domu = models.CharField(max_length=10, default='')
    licz_lokali = models.IntegerField(null=True)
    predkosc_max = models.CharField(max_length=10, default='', null=True)
    nazwa_ulicy = models.CharField(max_length=50, default='', null=True)
    uruchomienie = models.DateField(null=True)
    nazwa_gminy = models.CharField(max_length=100, default='')
    miejscowosc = models.CharField(max_length=100, default='')
    opis_budynku = models.TextField(max_length=1000, default='')
    typ_budynku = models.CharField(max_length=40, default='', null=True)
    handlowiec = models.CharField(max_length=40, default='')
    symbol = models.CharField(max_length=10, default='', null=True)
    technologia = models.CharField(max_length=40, default='', null=True)
    konkurencja = models.BooleanField(default=False)
    jaka_konkurencja = models.ManyToManyField(Konkurencja, related_name='konkurencje', related_query_name='konkurencje')
    data_dod = models.DateTimeField(default=datetime.date.today)

    def __str__(self):
        # return str(self.first_name) + ' ' + str(self.last_name) + ' (id: ' + str(self.pk) + ')'
        return str(self.nazwa_ulicy) + ' ' + str(self.numer_domu)


photo_upload = 'Ulotki/%Y/%m/%d'
photo_upload2 = 'Instalacje/%Y/%m/%d'


class Gminy(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa_gminy = models.CharField(max_length=30, default='', unique=True)
    ulotkarz = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.nazwa_gminy) + ' (' + str(self.ulotkarz) + ')'


class Ulotki(models.Model):
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True)
    uploaded_at = models.DateField(auto_now_add=True)
    opis = models.CharField(max_length=500, default='')
    ilosc = models.IntegerField(null=True)
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)


class Photo(models.Model):
    ulotki = models.ForeignKey(Ulotki, on_delete=models.CASCADE, default=None, null=True)
    file = models.ImageField(default=None, upload_to=photo_upload)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        new_image = compress(self.file)
        self.file = new_image
        super().save(*args, **kwargs)


class ProbyKontaktu(models.Model):
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True)
    numer_mieszkania = models.IntegerField()
    data_proby_kontaktu = models.DateTimeField(auto_now_add=True)
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)


class Instalacje(models.Model):
    poprzedni_numer_klienta = models.CharField(max_length=50, null=False)
    numer_klienta = models.IntegerField()
    data_instalacji = models.DateField(auto_now_add=True)
    notatka = models.CharField(max_length=400)
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)


class InstalacjeZdjecia(models.Model):
    instalacje = models.ForeignKey(Instalacje, on_delete=models.CASCADE, default=None, null=True)
    file = models.ImageField(default=None, upload_to=photo_upload2)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ident = models.IntegerField(default=None, null=True)

    def save(self, *args, **kwargs):
        new_image = compress(self.file)
        self.file = new_image
        super().save(*args, **kwargs)


class Lokale(models.Model):
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True)
    numer_mieszkania = models.IntegerField()
    nasz_klient = models.BooleanField(default=False)
    konkurencji_klient = models.BooleanField(default=False)
    data_kontaktu = models.DateTimeField(blank=True, null=True)
    data_konca_umowy = models.DateField(blank=True, null=True)
    data_kolejnego_kontaktu = models.DateField(blank=True, null=True)
    konkurencja = models.ForeignKey(Konkurencja, on_delete=models.CASCADE, null=True)
    klatka = models.CharField(max_length=10, blank=True, default='')
    imie_klienta = models.CharField(max_length=20, blank=True, null=True)
    telefon = models.IntegerField(blank=True, null=True)
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    data_dodania_wpisu = models.DateField(auto_now_add=True, blank=True, null=True)
    data_modyfikacji = models.DateTimeField(auto_now=True, blank=True, null=True)
    opis = models.CharField(max_length=200, default='', blank=True)
    price = models.FloatField(blank=True, verbose_name='Obecnie płaci', null=True)


class LokaleHistory(models.Model):
    id_adr_lokal = models.ForeignKey(Lokale, on_delete=models.CASCADE, null=True)
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True)
    numer_mieszkania = models.IntegerField()
    nasz_klient = models.BooleanField(default=False)
    konkurencji_klient = models.BooleanField(default=False)
    data_kontaktu = models.DateTimeField(blank=True, null=True)
    data_konca_umowy = models.DateField(blank=True, null=True)
    data_kolejnego_kontaktu = models.DateField(blank=True, null=True)
    konkurencja = models.ForeignKey(Konkurencja, on_delete=models.CASCADE, null=True)
    klatka = models.CharField(max_length=10, blank=True, default='')
    imie_klienta = models.CharField(max_length=20, blank=True, null=True)
    telefon = models.IntegerField(blank=True, null=True)
    uzytkownik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, null=True)
    data_dodania_wpisu = models.DateField(auto_now_add=True, blank=True, null=True)
    data_modyfikacji = models.DateTimeField(auto_now=True, blank=True, null=True)
    opis = models.CharField(max_length=200, default='', blank=True)
    price = models.FloatField(blank=True, verbose_name='Obecnie płaci', null=True)


class Symbole(models.Model):
    id_adr_dom_symbol = models.AutoField(primary_key=True)
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True)
    id_sprzedawca = models.ForeignKey(Sprzedawca, on_delete=models.CASCADE, verbose_name='Sprzedawca', null=True,
                                      blank=True)
    symbol = models.CharField(max_length=10)


class Typ(models.Model):
    id_adr_typ_budynku = models.AutoField(primary_key=True)
    nazwa_typu = models.CharField(max_length=50, unique=True)


class Budynek(models.Model):
    id_adr_budynek = models.AutoField(primary_key=True)
    id_adr_ulica = models.ForeignKey(Ulica, on_delete=models.CASCADE, verbose_name='Ulica', null=True, blank=True)
    id_adr_typ_budynku = models.ForeignKey(Typ, on_delete=models.CASCADE, verbose_name='Typ', null=True, blank=True)
    numer_budynku = models.CharField(max_length=10)
    opis_budynku = models.CharField(max_length=500, null=True)


class Handlowiec(models.Model):
    id_um_podpisujacy = models.AutoField(primary_key=True)
    imie = models.CharField(max_length=100)
    nazwisko = models.CharField(max_length=100)
    stanowisko = models.CharField(max_length=100)
    aktywny = models.CharField(max_length=10)


class Lokalizacja(models.Model):
    id_adr_dom_podpisujacy = models.AutoField(primary_key=True)
    id_sprzedawca = models.ForeignKey(Sprzedawca, on_delete=models.CASCADE, verbose_name='Sprzedawca', null=True,
                                      blank=True)
    id_adr_dom = models.ForeignKey(Dom, on_delete=models.CASCADE, verbose_name='Dom', null=True, blank=True, related_name='lokalizacja')
    id_um_podpisujacy = models.ForeignKey(Handlowiec, on_delete=models.CASCADE, verbose_name='Handlowiec', null=True,
                                          blank=True)


class ExternalModel(models.Model):
    class Meta:
        managed = False
        abstract = True
        app_label = 'remote'


class SortAdrDom(ExternalModel):
    id_adr_dom = models.AutoField(primary_key=True, db_column='id_adr_dom')
    licz_lokali = models.IntegerField(db_column='licz_lokali')
    numer_domu = models.TextField(db_column='numer_domu')
    predkosc_max = models.TextField(db_column='predkosc_max')
    id_adr_ulica = models.IntegerField(db_column='id_adr_ulica')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_dom"'


class SortAdrGmina(ExternalModel):
    id_adr_gmina = models.AutoField(primary_key=True, db_column='id_adr_gmina')
    nazwa_gminy = models.TextField(db_column='nazwa_gminy')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_gmina"'


class SortAdrUlica(ExternalModel):
    id_adr_ulica = models.AutoField(primary_key=True)
    id_adr_miejscowosc = models.IntegerField(db_column='id_adr_miejscowosc')
    typ = models.TextField(db_column='typ')
    nazwa_ulicy = models.TextField(db_column='nazwa_ulicy')
    nazwa_ulicy_1 = models.TextField(db_column='nazwa_ulicy_1')
    nazwa_ulicy_2 = models.TextField(db_column='nazwa_ulicy_2')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_ulica"'


class SortAdrBudynek(ExternalModel):
    id_adr_budynek = models.AutoField(primary_key=True)
    id_adr_ulica = models.IntegerField(db_column='id_adr_ulica')
    id_adr_typ_budynku = models.IntegerField(db_column='id_adr_typ_budynku')
    numer_budynku = models.TextField(db_column='numer_budynku')
    opis_budynku = models.TextField(db_column='opis_budynku')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_budynek"'


class SortAdrTypBudynku(ExternalModel):
    id_adr_typ_budynku = models.AutoField(primary_key=True)
    nazwa_typu = models.TextField(db_column='nazwa_typu')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_typ_budynku"'


class SortAdrMiejscowosc(ExternalModel):
    id_adr_miejscowosc = models.AutoField(primary_key=True)
    nazwa_miejscowosci = models.TextField(db_column='nazwa_miejscowosci')
    id_adr_gmina = models.TextField(db_column='id_adr_gmina')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_miejscowosc"'


class SortAdrDomPodpisujacy(ExternalModel):
    id_adr_dom_podpisujacy = models.AutoField(primary_key=True, db_column='id_adr_dom_podpisujacy')
    id_adr_dom = models.IntegerField(db_column='id_adr_dom')
    uruchomienie = models.DateField(db_column='uruchomienie')
    id_um_podpisujacy = models.IntegerField(db_column='id_um_podpisujacy')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_dom_podpisujacy"'


class SortUmPodpisujacy(ExternalModel):
    id_um_podpisujacy = models.AutoField(primary_key=True)
    imie = models.TextField(db_column='imie')
    nazwisko = models.TextField(db_column='nazwisko')
    stanowisko = models.TextField(db_column='stanowisko')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."um_podpisujacy"'


class SortAdrDomSymbol(ExternalModel):
    id_adr_dom_symbol = models.AutoField(primary_key=True)
    id_adr_dom = models.IntegerField(db_column='id_adr_dom')
    symbol = models.TextField(db_column='symbol')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_dom_symbol"'


class SortAdrDomTechnologia(ExternalModel):
    id_adr_dom_technologia = models.AutoField(primary_key=True)
    id_adr_dom = models.IntegerField(db_column='id_adr_dom')
    id_gniazdka_technologie = models.IntegerField(db_column='id_gniazdka_technologie')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."adr_dom_technologia"'


class SortGniazdkaTechnologie(ExternalModel):
    id_gniazdka_technologie = models.AutoField(primary_key=True)
    nazwa = models.TextField(db_column='nazwa')

    class Meta(ExternalModel.Meta):
        db_table = '"USORT4"."gniazdka_technologie"'