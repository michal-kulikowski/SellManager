from django.utils import timezone

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from core.models import Instalacje, InstalacjeZdjecia, Ulotki, Photo, Lokale, Dom
from django.contrib.auth.decorators import login_required

from panel_lokalizacji.forms import DateForm
from templates.metody.metody import has_group


@login_required
def raporty(request):
    context = {

    }

    return render(request, 'raporty/raporty-dashboard.html', context)


@login_required
def raport_instalacje(request):
    now = timezone.now()
    if request.method == 'POST':
        year = ''
        month = ''
        form = DateForm(request.POST)
        if form.is_valid():
            pass
        else:
            year = form.data.get('year')
            month = form.data.get('month')
        if year != '' and month != '':
            instalacje = Instalacje.objects.filter(data_instalacji__year=year, data_instalacji__month=month)
        if year == '' and month != '':
            instalacje = Instalacje.objects.filter(data_instalacji__year=now.year, data_instalacji__month=month)
        if year != '' and month == '':
            instalacje = Instalacje.objects.filter(data_instalacji__year=year)
        if year == '' and month == '':
            instalacje = Instalacje.objects.all().order_by('-id')

    else:
        form = DateForm()
        instalacje = Instalacje.objects.filter(data_instalacji__year=now.year,
                                               data_instalacji__month=now.month).order_by('-id')

    context = {
        'form': form,
        'instalacje': instalacje,
    }

    return render(request, 'raporty/raport-instalacje.html', context)


@login_required
def zdjecia_instalacja_redirect(request, getIdFromRow):
    request.session['id_instalacji'] = getIdFromRow

    return redirect('raporty:zdjecia_instalacja')


@login_required
def zdjecia_instalacja(request):
    id_instalacji = request.session.get('id_instalacji')
    instalacja = Instalacje.objects.get(id=id_instalacji)
    photos = InstalacjeZdjecia.objects.filter(instalacje_id=id_instalacji)

    context = {
        'photos': photos,
        'instalacja': instalacja,
    }

    return render(request, 'raporty/zdjecia-instalacje.html', context)


@login_required
def raport_ulotki(request):
    now = timezone.now()
    if request.method == 'POST':
        year = ''
        month = ''
        form = DateForm(request.POST)
        if form.is_valid():
            pass
        else:
            year = form.data.get('year')
            month = form.data.get('month')
        if year != '' and month != '':
            ulotki = Ulotki.objects.filter(uploaded_at__year=year, uploaded_at__month=month)
        if year == '' and month != '':
            ulotki = Ulotki.objects.filter(uploaded_at__year=now.year, uploaded_at__month=month)
        if year != '' and month == '':
            ulotki = Ulotki.objects.filter(uploaded_at__year=year)
        if year == '' and month == '':
            ulotki = Ulotki.objects.all().order_by('-id')

    else:
        form = DateForm()
        ulotki = Ulotki.objects.filter(uploaded_at__year=now.year, uploaded_at__month=now.month).order_by('-id')

    context = {
        'form': form,
        'ulotki': ulotki,
    }

    return render(request, 'raporty/raport-ulotek.html', context)


@login_required
def raport_leady(request):
    now = timezone.now()
    if request.method == 'POST':
        year = ''
        month = ''
        form = DateForm(request.POST)
        if form.is_valid():
            pass
        else:
            year = form.data.get('year')
            month = form.data.get('month')
        if year != '' and month != '':
            leady = Lokale.objects.filter(data_dodania_wpisu__year=year, data_dodania_wpisu__month=month)
        if year == '' and month != '':
            leady = Lokale.objects.filter(data_dodania_wpisu__year=now.year, data_dodania_wpisu__month=month)
        if year != '' and month == '':
            leady = Lokale.objects.filter(data_dodania_wpisu__year=year)
        if year == '' and month == '':
            leady = Lokale.objects.all().order_by('-id')

    else:
        form = DateForm()
        leady = Lokale.objects.filter(data_dodania_wpisu__year=now.year, data_dodania_wpisu__month=now.month).order_by(
            '-id')

    context = {
        'form': form,
        'leady': leady,
    }

    return render(request, 'raporty/raport-leadow.html', context)


@login_required
def zdjecia_ulotek_redirect(request, getIdFromRow):
    request.session['id_ulotki'] = getIdFromRow

    return redirect('raporty:zdjecia_ulotek')


@login_required
def zdjecia_ulotek(request):
    id_ulotki = request.session.get('id_ulotki')
    ulotka = Ulotki.objects.get(id=id_ulotki)
    photos = Photo.objects.filter(ulotki_id=id_ulotki)

    context = {
        'photos': photos,
        'ulotka': ulotka,
    }

    return render(request, 'raporty/zdjecia-ulotki.html', context)


from datetime import datetime, timedelta


@login_required
def lokalizacje_bez_ulotek(request):
    if has_group(request.user, 'Handlowcy'):
        lokalizacje_bez_ulotek = Dom.objects.filter(licz_lokali__gte=7).filter(
            handlowiec=(request.user.first_name + ' ' + request.user.last_name)).exclude(
            ulotki__uploaded_at__gte=datetime.now() - timedelta(days=14)).exclude(nazwa_ulicy__icontains='Szkolna')
        context = {
            'lokalizacje_bez_ulotek': lokalizacje_bez_ulotek,
        }
        return render(request, 'raporty/raport-braku-ulotek-ph.html', context)
    else:
        lokalizacje_bez_ulotek = Dom.objects.filter(licz_lokali__gte=7).exclude(
            ulotki__uploaded_at__gte=datetime.now() - timedelta(days=14)).exclude(nazwa_ulicy__icontains='Szkolna')

    context = {
        'lokalizacje_bez_ulotek': lokalizacje_bez_ulotek,
    }
    return render(request, 'raporty/raport-braku-ulotek.html', context)
