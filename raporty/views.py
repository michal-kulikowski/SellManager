from django.shortcuts import render, redirect

# Create your views here.
from core.models import Instalacje, InstalacjeZdjecia, Ulotki, Photo


def raporty(request):

    context = {

    }

    return render(request, 'raporty/raporty-dashboard.html', context)


def raport_instalacje(request):
    instalacje = Instalacje.objects.all().order_by('-id')

    context = {
        'instalacje': instalacje,
    }

    return render(request, 'raporty/raport-instalacje.html', context)


def zdjecia_instalacja_redirect(request, getIdFromRow):
    request.session['id_instalacji'] = getIdFromRow

    return redirect('raporty:zdjecia_instalacja')


def zdjecia_instalacja(request):
    id_instalacji = request.session.get('id_instalacji')
    instalacja = Instalacje.objects.get(id=id_instalacji)
    photos = InstalacjeZdjecia.objects.filter(instalacje_id=id_instalacji)

    context = {
        'photos': photos,
        'instalacja': instalacja,
    }

    return render(request, 'raporty/zdjecia-instalacje.html', context)


def raport_ulotki(request):
    ulotki = Ulotki.objects.all().order_by('-id')

    context = {
        'ulotki': ulotki,
    }

    return render(request, 'raporty/raport-ulotek.html', context)


def zdjecia_ulotek_redirect(request, getIdFromRow):
    request.session['id_ulotki'] = getIdFromRow

    return redirect('raporty:zdjecia_ulotek')


def zdjecia_ulotek(request):
    id_ulotki = request.session.get('id_ulotki')
    ulotka = Ulotki.objects.get(id=id_ulotki)
    photos = Photo.objects.filter(ulotki_id=id_ulotki)

    context = {
        'photos': photos,
        'ulotka': ulotka,
    }

    return render(request, 'raporty/zdjecia-ulotki.html', context)