from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import FormView

from core.models import Dom, Symbole, Sprzedawca, SortAdrDomPodpisujacy, SortAdrDom, SortAdrUlica, SortAdrMiejscowosc, \
    SortAdrBudynek, SortAdrTypBudynku, SortUmPodpisujacy, SortAdrDomSymbol, SortAdrDomTechnologia, \
    SortGniazdkaTechnologie, Lokale, LokaleHistory, Ulotki, Photo, ProbyKontaktu
from edit_app.forms import EditDomForm, EditSymbolForm, LokalForm, FileFieldForm, ProbaForm


def edit_dom_redirect(request, getIdFromRow, liczba_klientow):
    request.session['dom_id'] = getIdFromRow
    request.session['ilosc_klientow'] = liczba_klientow
    return redirect('edit_app:edit_dom')


def edit_dom_redirect_ulotki(request, getIdFromRow, liczba_klientow):
    dom_id = Ulotki.objects.get(id=getIdFromRow).id_adr_dom.id_adr_dom
    request.session['dom_id'] = dom_id
    request.session['ilosc_klientow'] = liczba_klientow
    return redirect('edit_app:edit_dom')


def edit_dom(request):
    dom_id = request.session.get('dom_id')
    ilosc_klientow = request.session.get('ilosc_klientow')
    ulotki = Ulotki.objects.filter(id_adr_dom_id=dom_id).order_by('-id')
    proby_kontaktu = ProbyKontaktu.objects.filter(id_adr_dom_id=dom_id).order_by('-id')
    try:
        last_ulotka = Ulotki.objects.filter(id_adr_dom_id=dom_id).order_by('-id')[0]
    except IndexError:
        last_ulotka = None
    numer_domu = SortAdrDom.objects.get(id_adr_dom=dom_id).numer_domu
    licz_lokali = SortAdrDom.objects.get(id_adr_dom=dom_id).licz_lokali
    predkosc_max = SortAdrDom.objects.get(id_adr_dom=dom_id).predkosc_max
    nazwa_ulicy = SortAdrUlica.objects.get(
        id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica).nazwa_ulicy
    miejscowosc = SortAdrMiejscowosc.objects.get(id_adr_miejscowosc=SortAdrUlica.objects.get(
        id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica).id_adr_miejscowosc).nazwa_miejscowosci
    try:
        typ_budynku = SortAdrTypBudynku.objects.get(id_adr_typ_budynku=SortAdrBudynek.objects.get(id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica, numer_budynku=SortAdrDom.objects.get(id_adr_dom=dom_id).numer_domu).id_adr_typ_budynku).nazwa_typu
    except ObjectDoesNotExist:
        typ_budynku = 'Brak'
    try:
        symbol = SortAdrDomSymbol.objects.filter(id_adr_dom=dom_id)[0].symbol
    except IndexError:
        symbol = 'Brak'
    uruchomienie = SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[0].uruchomienie
    try:
        technologia = SortGniazdkaTechnologie.objects.get(
            id_gniazdka_technologie=SortAdrDomTechnologia.objects.get(id_adr_dom=dom_id).id_gniazdka_technologie).nazwa
    except SortAdrDomTechnologia.DoesNotExist:
        technologia = 'Brak'
    handlowiec = SortUmPodpisujacy.objects.get(
        id_um_podpisujacy=SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[
            0].id_um_podpisujacy).imie + ' ' + SortUmPodpisujacy.objects.get(
        id_um_podpisujacy=SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[0].id_um_podpisujacy).nazwisko

    if Dom.objects.filter(id_adr_dom=dom_id).exists():
        dom = Dom.objects.filter(id_adr_dom=dom_id)
        if ilosc_klientow != 'Brak':
            dom.update(id_adr_dom=dom_id, numer_domu=numer_domu, licz_lokali=licz_lokali, predkosc_max=predkosc_max, nazwa_ulicy=nazwa_ulicy, uruchomienie=uruchomienie, miejscowosc=miejscowosc, typ_budynku=typ_budynku, handlowiec=handlowiec, ilosc_klientow=ilosc_klientow, symbol=symbol, technologia=technologia)
            dom = Dom.objects.get(id_adr_dom=dom_id)
        else:
            dom = Dom.objects.get(id_adr_dom=dom_id)
    else:
        if ilosc_klientow != 'Brak':
            Dom.objects.create(id_adr_dom=dom_id, numer_domu=numer_domu, licz_lokali=licz_lokali, predkosc_max=predkosc_max, nazwa_ulicy=nazwa_ulicy, uruchomienie=uruchomienie, miejscowosc=miejscowosc, typ_budynku=typ_budynku, handlowiec=handlowiec, ilosc_klientow=ilosc_klientow, symbol=symbol, technologia=technologia)
            dom = Dom.objects.get(id_adr_dom=dom_id)
        else:
            dom = Dom.objects.get(id_adr_dom=dom_id)

    lokale = Lokale.objects.filter(id_adr_dom=dom_id)

    if request.method == 'POST':
        form_dom = EditDomForm(request.POST, instance=dom)
        if form_dom.is_valid():
            form_dom.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')

    else:
        form_dom = EditDomForm(instance=dom)

    context = {
        'form_dom': form_dom,
        'dom': dom,
        'lokale': lokale,
        'ulotki': ulotki,
        'last_ulotka': last_ulotka,
        'proby_kontaktu': proby_kontaktu,
    }
    return render(request, 'edit_app/edit-dom.html', context)


def dodaj_informacje_klient(request):
    dom_id = request.session.get('dom_id')

    if request.method == 'POST':
        form_lokal = LokalForm(request.POST)
        if form_lokal.is_valid():
            form = form_lokal.save(commit=False)
            form.id_adr_dom = Dom.objects.get(id_adr_dom=dom_id)
            if Lokale.objects.filter(id_adr_dom=dom_id, numer_mieszkania=form.numer_mieszkania):
                lokal = Lokale.objects.get(id_adr_dom=dom_id, numer_mieszkania=form.numer_mieszkania)
                lokal.nasz_klient = form.nasz_klient
                lokal.konkurencji_klient = form.konkurencji_klient
                lokal.data_kontaktu = form.data_kontaktu
                lokal.data_kolejnego_kontaktu = form.data_kolejnego_kontaktu
                lokal.data_konca_umowy = form.data_konca_umowy
                lokal.konkurencja = form.konkurencja
                lokal.klatka = form.klatka
                lokal.imie_klienta = form.imie_klienta
                lokal.telefon = form.telefon
                lokal.data_modyfikacji = form.data_modyfikacji
                lokal.opis = form.opis
                lokal.price = form.price
                lokal.uzytkownik = request.user
                LokaleHistory.objects.create(
                    id_adr_lokal=Lokale.objects.get(id_adr_dom=dom_id, numer_mieszkania=form.numer_mieszkania),
                    numer_mieszkania=form.numer_mieszkania, nasz_klient=form.nasz_klient,
                    konkurencji_klient=form.konkurencji_klient,
                    data_kontaktu=form.data_kontaktu, data_kolejnego_kontaktu=form.data_kolejnego_kontaktu,
                    data_konca_umowy=form.data_konca_umowy, konkurencja=form.konkurencja, klatka=form.klatka,
                    uzytkownik=request.user, data_modyfikacji=form.data_modyfikacji,
                    opis=form.opis, price=form.price)
                lokal.save()
                return redirect('edit_app:edit_dom')
            else:
                form.uzytkownik = request.user
                form.save()
                LokaleHistory.objects.create(
                    id_adr_lokal=Lokale.objects.get(id_adr_dom=dom_id, numer_mieszkania=form.numer_mieszkania),
                    numer_mieszkania=form.numer_mieszkania, nasz_klient=form.nasz_klient,
                    konkurencji_klient=form.konkurencji_klient,
                    data_kontaktu=form.data_kontaktu, data_kolejnego_kontaktu=form.data_kolejnego_kontaktu,
                    data_konca_umowy=form.data_konca_umowy, konkurencja=form.konkurencja, klatka=form.klatka,
                    imie_klienta=form.imie_klienta, telefon=form.telefon,
                    uzytkownik=request.user, data_modyfikacji=form.data_modyfikacji,
                    opis=form.opis, price=form.price)
            # return HttpResponse('<script type="text/javascript">window.close()</script>')
            return redirect('edit_app:edit_dom')
    else:
        form_lokal = LokalForm()

    context = {
        'form_lokal': form_lokal,
    }

    return render(request, 'edit_app/edit-lokal.html', context)


def show_lokal_redirect(request, getIdFromRow):
    request.session['lokal_id'] = getIdFromRow
    return redirect('edit_app:show_lokal')


def show_lokal(request):
    ilosc_klientow = request.session.get('ilosc_klientow')
    lokal_id = request.session.get('lokal_id')
    dom_id = request.session.get('dom_id')
    try:
        last_ulotka = Ulotki.objects.filter(id_adr_dom_id=dom_id).order_by('-id')[0]
    except IndexError:
        last_ulotka = None
    numer_domu = SortAdrDom.objects.get(id_adr_dom=dom_id).numer_domu
    licz_lokali = SortAdrDom.objects.get(id_adr_dom=dom_id).licz_lokali
    predkosc_max = SortAdrDom.objects.get(id_adr_dom=dom_id).predkosc_max
    nazwa_ulicy = SortAdrUlica.objects.get(
        id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica).nazwa_ulicy
    miejscowosc = SortAdrMiejscowosc.objects.get(id_adr_miejscowosc=SortAdrUlica.objects.get(
        id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica).id_adr_miejscowosc).nazwa_miejscowosci
    try:
        typ_budynku = SortAdrTypBudynku.objects.get(id_adr_typ_budynku=SortAdrBudynek.objects.get(id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=dom_id).id_adr_ulica, numer_budynku=SortAdrDom.objects.get(id_adr_dom=dom_id).numer_domu).id_adr_typ_budynku).nazwa_typu
    except ObjectDoesNotExist:
        typ_budynku = 'Brak'
    try:
        symbol = SortAdrDomSymbol.objects.filter(id_adr_dom=dom_id)[0].symbol
    except IndexError:
        symbol = 'Brak'
    uruchomienie = SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[0].uruchomienie
    technologia = SortGniazdkaTechnologie.objects.get(
        id_gniazdka_technologie=SortAdrDomTechnologia.objects.get(id_adr_dom=dom_id).id_gniazdka_technologie).nazwa
    handlowiec = SortUmPodpisujacy.objects.get(
        id_um_podpisujacy=SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[
            0].id_um_podpisujacy).imie + ' ' + SortUmPodpisujacy.objects.get(
        id_um_podpisujacy=SortAdrDomPodpisujacy.objects.filter(id_adr_dom=dom_id)[0].id_um_podpisujacy).nazwisko
    if Dom.objects.filter(id_adr_dom=dom_id).exists():
        dom = Dom.objects.filter(id_adr_dom=dom_id)
        dom.update(id_adr_dom=dom_id, numer_domu=numer_domu, licz_lokali=licz_lokali, predkosc_max=predkosc_max,
                   nazwa_ulicy=nazwa_ulicy, uruchomienie=uruchomienie, miejscowosc=miejscowosc, typ_budynku=typ_budynku,
                   handlowiec=handlowiec, ilosc_klientow=ilosc_klientow, symbol=symbol, technologia=technologia)
        dom = Dom.objects.get(id_adr_dom=dom_id)
    else:
        Dom.objects.create(id_adr_dom=dom_id, numer_domu=numer_domu, licz_lokali=licz_lokali, predkosc_max=predkosc_max,
                           nazwa_ulicy=nazwa_ulicy, uruchomienie=uruchomienie, miejscowosc=miejscowosc,
                           typ_budynku=typ_budynku,
                           handlowiec=handlowiec, ilosc_klientow=ilosc_klientow, symbol=symbol, technologia=technologia)
        dom = Dom.objects.get(id_adr_dom=dom_id)

    lokale = LokaleHistory.objects.filter(id_adr_lokal=lokal_id).order_by('-id')
    lokal = Lokale.objects.get(id=lokal_id)

    if request.method == 'POST':
        form_dom = EditDomForm(request.POST, instance=dom)
        if form_dom.is_valid():
            form_dom.save()
            return HttpResponse('<script type="text/javascript">window.close()</script>')

    else:
        form_dom = EditDomForm(instance=dom)

    context = {
        'form_dom': form_dom,
        'dom': dom,
        'lokale': lokale,
        'lokal': lokal,
        'last_ulotka': last_ulotka,
    }
    return render(request, 'edit_app/show-lokal.html', context)


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'edit_app/ulotki-upload-photos.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        dom_id = request.session.get('dom_id')
        if form.is_valid():
            if len(files) > 5:
                msg = 'Możesz dodać maksymalnie 5 zdjęć'
                return render(request, 'edit_app/error-page.html',
                              {'error_message': msg})
            else:
                ulotki = Ulotki.objects.create(id_adr_dom_id=dom_id, ilosc=form.cleaned_data.get('ilosc'),
                                               uzytkownik=request.user, opis=form.cleaned_data.get('opis'))
                for f in files:
                    Photo.objects.create(file=f, ulotki_id=ulotki.id)

                return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dom_id'] = self.request.session['dom_id']
        return context

    def get_success_url(self):
        return reverse('edit_app:edit_dom')


def show_ulotki_photos_redirect(request, getIdFromRow):
    request.session['ulotki_id'] = getIdFromRow
    return redirect('edit_app:show_ulotki_photos')


def show_ulotki_photos(request):
    ulotki_id = request.session.get('ulotki_id')
    ulotki = Ulotki.objects.filter(id=ulotki_id)
    photos = Photo.objects.filter(ulotki_id=ulotki_id)

    context = {
        'ulotki': ulotki,
        'photos': photos,
    }

    # return HttpResponse(ulotki)
    return render(request, 'edit_app/show-ulotki-photos.html', context)


def dodaj_probe_kontaktu(request):
    dom_id = request.session.get('dom_id')

    if request.method == 'POST':
        form_proba = ProbaForm(request.POST)
        if form_proba.is_valid():
            object = form_proba.save(commit=False)
            object.id_adr_dom_id = dom_id
            object.uzytkownik = request.user
            object.save()

            return redirect('edit_app:edit_dom')
    else:
        form_proba = ProbaForm()

    context = {
        'form_proba': form_proba,
    }

    return render(request, 'edit_app/lokal-proba-kontaktu.html', context)
