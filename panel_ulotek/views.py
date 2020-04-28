import json

from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

# Create your views here.
from django.urls import reverse

from core.models import Dom
from panel_ulotek.forms import UlotkiForm
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
            test = form.cleaned_data['osoba']
            request.session['ulotkarz'] = json.dumps(test)
            return redirect('panel_ulotek:formularz_gminy')
    else:
        form = UlotkiForm()

    context = {
        'form': form,
    }

    return render(request, 'panel_ulotek/przypisz_gminy.html', context)


def formularz_gminy(request):
    ulotkarz = request.session.get('ulotkarz')

    form = UlotkiForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            return HttpResponse('test')
    else:
        form = UlotkiForm()

    context = {
        'form': form,
    }

    return render(request, 'panel_ulotek/formularz-gminy.html', context)