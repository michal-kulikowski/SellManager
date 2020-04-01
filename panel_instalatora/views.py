from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import FormView

from core.models import InstalacjeZdjecia, Instalacje
from panel_instalatora.forms import InstalacjaForm, FileFieldFormInstalacje


@login_required
def panel_instalatora(request):
    instalacje = Instalacje.objects.filter(uzytkownik=request.user)

    context = {
        'instalacje': instalacje,
    }
    return render(request, 'panel_instalatora/panel_instalatora.html', context)


@login_required
def formularz_instalacji(request):
    if request.method == 'POST':
        form = InstalacjaForm(request.POST)
        if form.is_valid():
            dane_formularz = form.save(commit=False)
            poprzedni_numer = dane_formularz.poprzedni_numer_klienta
            numer_klienta = dane_formularz.numer_klienta
            notatka = dane_formularz.notatka
            request.session['poprzedni_numer'] = poprzedni_numer.upper()
            request.session['numer_klienta'] = numer_klienta
            request.session['notatka'] = notatka

            return redirect('panel_instalatora:dodanie-zdjec-instalacji')
            # return HttpResponse(poprzedni_numer)
        else:
            return HttpResponse("nie sukces")
    else:
        form = InstalacjaForm()

    context = {
        'form': form,
    }

    return render(request, 'panel_instalatora/formularz-instalacji.html', context)


# @login_required
class FileFieldView(FormView):
    form_class = FileFieldFormInstalacje
    template_name = 'panel_instalatora/dodanie-zdjec-instalacji.html'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            cache = InstalacjeZdjecia.objects.filter(ident=100)
            cache.delete()
            if len(files) > 6:
                msg = 'Możesz dodać maksymalnie 6 zdjęć'
                return render(request, 'edit_app/error-page.html',
                              {'error_message': msg})
            else:
                for f in files:
                    InstalacjeZdjecia.objects.create(file=f, ident=100)
                return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('panel_instalatora:potwierdzenie_formularza_instalacji')


@login_required
def potwierdzenie_formularza_instalacji(request):
    poprzedni_numer = request.session.get('poprzedni_numer')
    numer_klienta = request.session.get('numer_klienta')
    notatka = request.session.get('notatka')
    photos = InstalacjeZdjecia.objects.filter(ident=100)

    if request.method == 'POST':
                object = Instalacje.objects.create(poprzedni_numer_klienta=poprzedni_numer, numer_klienta=numer_klienta, notatka=notatka, uzytkownik=request.user)
                photos.update(instalacje_id=object.id)
                photos.update(ident=None)
                return redirect('panel_instalatora:panel_instalatora')
    else:
        pass
    context = {
        'photos': photos,
        'poprzedni_numer': poprzedni_numer,
        'numer_klienta': numer_klienta,
        'notatka': notatka,
    }
    return render(request, 'panel_instalatora/zatwierdzenie-formularza-instalacji.html', context)


@login_required
def show_photos_instalacja_redirect(request, getIdFromRow):
    request.session['id_instalacji'] = getIdFromRow

    return redirect('panel_instalatora:show_photos_instalacja')


@login_required
def show_photos_instalacja(request):
    id_instalacji = request.session.get('id_instalacji')
    instalacja = Instalacje.objects.get(id=id_instalacji)
    photos = InstalacjeZdjecia.objects.filter(instalacje_id=id_instalacji)

    context = {
        'photos': photos,
        'instalacja': instalacja,
    }

    return render(request, 'panel_instalatora/show-photos-instalacje.html', context)