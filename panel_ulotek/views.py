import json

from django.contrib.auth.models import Group
from django.db.models import Exists, Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

# Create your views here.
from django.urls import reverse

from core.models import Dom, Gminy
from panel_ulotek.forms import UlotkiForm, GminyForm
from users.models import User


def base(request):
    lokalizacje_bez_ulotek = Dom.objects.filter(licz_lokali__gte=7).exclude(
        ulotki__uploaded_at__gte=datetime.now() - timedelta(days=14)).exclude(nazwa_ulicy__icontains='Szkolna').filter(handlowiec__icontains='Handlowy')

    context = {
        'lokalizacje_bez_ulotek': lokalizacje_bez_ulotek,
    }

    return render(request, 'panel_ulotek/ulotkarz.html', context)


def przypisz_gminy(request):
    form = UlotkiForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_id = form.data.get('osoba')
            request.session['ulotkarz'] = user_id
            return redirect('panel_ulotek:formularz_gminy')
    else:
        form = UlotkiForm()

    context = {
        'form': form,
    }

    return render(request, 'panel_ulotek/przypisz_gminy.html', context)


def formularz_gminy(request):
    user_id = request.session.get('user_id')

    form = GminyForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            pass
            # return HttpResponse('test')
    else:
        form = GminyForm()

    context = {
        'form': form,
    }

    return render(request, 'panel_ulotek/formularz-gminy.html', context)


def ulotkarz(request):
    user_lokalizacje = Gminy.objects.filter(ulotkarz=request.user)
    if not user_lokalizacje:
        return HttpResponse('Nie masz przypisanej żadnej dzielnicy')
    else:
        filtr_gmina_ulotkarz = Q()
        for nazwa_gminy in user_lokalizacje:
            filtr_gmina_ulotkarz = filtr_gmina_ulotkarz | Q(nazwa_gminy=nazwa_gminy.nazwa_gminy)
        lokalizacje_bez_ulotek = Dom.objects.filter(licz_lokali__gte=7).exclude(ulotki__uploaded_at__gte=datetime.now() - timedelta(days=14)).exclude(nazwa_ulicy__icontains='Szkolna').filter(handlowiec__icontains='Handlowy').filter(filtr_gmina_ulotkarz)

        context = {
            'lokalizacje_bez_ulotek': lokalizacje_bez_ulotek,
        }

        return render(request, 'panel_ulotek/ulotkarz.html', context)