from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render

from core.models import Lokalizacja, Dom, SortAdrDom, SortAdrDomPodpisujacy
from panel_lokalizacji.forms import SearchForm


def lokalizacje_list(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if request.user.groups.filter(name='Handlowcy'):
                handlowiec = request.user.last_name
                form.initial['handlowiec'] = request.user.last_name
            else:
                handlowiec = form.cleaned_data.get('handlowiec')
            ulica =  form.cleaned_data.get('ulica')
            symbol = form.cleaned_data.get('symbol')
            miejscowosc = form.cleaned_data.get('miejscowosc')
            predkosc_max_od = form.cleaned_data.get('predkosc_od')
            predkosc_max_do = form.cleaned_data.get('predkosc_do')
            hp_od = form.cleaned_data.get('hp_od')
            hp_do = form.cleaned_data.get('hp_do')
            wypelnienie_od = form.cleaned_data.get('wypelnienie_od')
            wypelnienie_do = form.cleaned_data.get('wypelnienie_do')
            liczba_klientow_od = form.cleaned_data.get('liczba_klientow_od')
            liczba_klientow_do = form.cleaned_data.get('liczba_klientow_do')
            uruchomienie_od = form.cleaned_data.get('uruchomienie_od')
            uruchomienie_do = form.cleaned_data.get('uruchomienie_do')
            handlowiec_query = " WHERE handlowiec.nazwisko LIKE '%%" + handlowiec + "%%'"
            if ulica != '':
                ulica_query = " AND ulica.nazwa_ulicy LIKE '%%" + ulica + "%%'"
            else:
                ulica_query = ""

            if miejscowosc != '':
                miejscowosc_query = " AND miejscowosc.nazwa_miejscowosci LIKE '%%" + miejscowosc + "%%'"
            else:
                miejscowosc_query = ""
            if symbol != '':
                symbol_query = " AND symbol.symbol LIKE '" + symbol + "'"
            else:
                symbol_query = ""

            if predkosc_max_od is not None or predkosc_max_do is not None:
                if predkosc_max_od is not None and predkosc_max_do is None:
                    predkosc_query = " AND dom.predkosc_max >= '" + str(predkosc_max_od) + "' "
                if predkosc_max_od is None and predkosc_max_do is not None:
                    predkosc_query = " AND dom.predkosc_max <= '" + str(predkosc_max_do) + "' "
                if predkosc_max_od is not None and predkosc_max_do is not None:
                    predkosc_query = " AND dom.predkosc_max BETWEEN '" + str(predkosc_max_od) + "' AND '" + str(predkosc_max_do) + "' "
            else:
                predkosc_query = ""

            if hp_od is not None or hp_do is not None:
                if hp_od == 0 and hp_do == 0:
                    hp_query = " AND dom.LICZ_LOKALI IS NULL"
                else:
                    if hp_od is not None and hp_do is None:
                        hp_query = " AND dom.LICZ_LOKALI >= '" + str(hp_od) + "' "
                    if hp_od is None and hp_do is not None:
                        hp_query = " AND (dom.LICZ_LOKALI <= '" + str(hp_do) + "' OR dom.LICZ_LOKALI IS NULL) "
                    if hp_od is not None and hp_do is not None and hp_od != 0 and hp_do != 0:
                        hp_query = " AND dom.LICZ_LOKALI BETWEEN '" + str(hp_od) + "' AND '" + str(hp_do) + "' "
                    if hp_od == 0 and hp_do != 0 and hp_do is not None:
                        hp_query = " AND (dom.LICZ_LOKALI IS NULL OR dom.LICZ_LOKALI <= '" + str(hp_do) + "')"
                    if hp_od == 0 and hp_do is None:
                        hp_query = ""
                    if hp_od != 0 and hp_do == 0:
                        hp_query = " AND dom.LICZ_LOKALI IS NULL"
                    if hp_od and hp_do == 0:
                        hp_query = " AND dom.LICZ_LOKALI IS NULL"
            else:
                hp_query = ""

            if liczba_klientow_od is not None or liczba_klientow_do is not None:
                if liczba_klientow_od == 0 and liczba_klientow_do == 0:
                    liczba_klientow_query = " AND LICZBA_KLIENTOW IS NULL"
                else:
                    if liczba_klientow_od is not None and liczba_klientow_do is None:
                        liczba_klientow_query = " AND LICZBA_KLIENTOW >= '" + str(liczba_klientow_od) + "' "
                    if liczba_klientow_od is None and liczba_klientow_do is not None:
                        liczba_klientow_query = " AND (LICZBA_KLIENTOW <= '" + str(liczba_klientow_do) + "' OR LICZBA_KLIENTOW IS NULL) "
                    if liczba_klientow_od is not None and liczba_klientow_do is not None and liczba_klientow_od != 0 and liczba_klientow_do != 0:
                        liczba_klientow_query = " AND LICZBA_KLIENTOW BETWEEN '" + str(liczba_klientow_od) + "' AND '" + str(liczba_klientow_do) + "' "
                    if liczba_klientow_od == 0 and liczba_klientow_do != 0 and liczba_klientow_do is not None:
                        liczba_klientow_query = " AND (LICZBA_KLIENTOW IS NULL OR LICZBA_KLIENTOW <= '" + str(liczba_klientow_do) + "')"
                    if liczba_klientow_od == 0 and liczba_klientow_do is None:
                        liczba_klientow_query = ""
                    if liczba_klientow_od != 0 and liczba_klientow_do == 0:
                        liczba_klientow_query = " AND LICZBA_KLIENTOW IS NULL"
                    if liczba_klientow_od and liczba_klientow_do == 0:
                        liczba_klientow_query = " AND LICZBA_KLIENTOW IS NULL"
            else:
                liczba_klientow_query = ""

            if uruchomienie_od is not None or uruchomienie_do is not None:
                    if uruchomienie_od is not None and uruchomienie_do is None:
                        uruchomienie_query = " AND lokalizacja.uruchomienie >= '" + str(uruchomienie_od) + "' "
                    if uruchomienie_od is None and uruchomienie_do is not None:
                        uruchomienie_query = " AND (lokalizacja.uruchomienie <= '" + str(uruchomienie_do) + "'"
                    if uruchomienie_od is not None and uruchomienie_do is not None:
                        uruchomienie_query = " AND lokalizacja.uruchomienie BETWEEN '" + str(uruchomienie_od) + "' AND '" + str(uruchomienie_do) + "' "
            else:
                uruchomienie_query = ""

            dom = SortAdrDomPodpisujacy.objects.raw("SELECT lokalizacja.ID_ADR_DOM_PODPISUJACY AS id_adr_dom_podpisujacy, dane_osobowe.NAZWA_KLIENTA AS NAZWA_SPRZEDAWCY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.id_adr_dom, dom.NUMER_DOMU, symbol.SYMBOL, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(klienci.LICZBA_KLIENTOW, 0) AS LICZBA_KLIENTOW, dom.PREDKOSC_MAX, handlowiec.IMIE, handlowiec.NAZWISKO, technologie.TECHNOLOGIE, lokalizacja.URUCHOMIENIE FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.DANE_OSOBOWE dane_osobowe ON sprzedawca.ID_DANE_OSOBOWE = dane_osobowe.ID_DANE_OSOBOWE LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM  LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM" + handlowiec_query + ulica_query + miejscowosc_query + symbol_query + predkosc_query + hp_query + liczba_klientow_query + uruchomienie_query + ";")
            # return HttpResponse(dom.raw_query)
    else:
        form = SearchForm()
        if request.user.groups.filter(name='Handlowcy'):
            handlowiec = '%' + request.user.last_name + '%'
            form.initial['handlowiec'] = request.user.last_name
            ulica = "%"
            miejscowosc = "%"
            dom = SortAdrDomPodpisujacy.objects.raw('''SELECT lokalizacja.ID_ADR_DOM_PODPISUJACY AS id_adr_dom_podpisujacy, dane_osobowe.NAZWA_KLIENTA AS NAZWA_SPRZEDAWCY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.id_adr_dom, dom.NUMER_DOMU, symbol.SYMBOL, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(klienci.LICZBA_KLIENTOW, 0) AS LICZBA_KLIENTOW, dom.PREDKOSC_MAX, handlowiec.IMIE, handlowiec.NAZWISKO, technologie.TECHNOLOGIE FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.DANE_OSOBOWE dane_osobowe ON sprzedawca.ID_DANE_OSOBOWE = dane_osobowe.ID_DANE_OSOBOWE LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM  LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM WHERE handlowiec.nazwisko LIKE %s AND ulica.nazwa_ulicy LIKE %s AND miejscowosc.nazwa_miejscowosci LIKE %s''',[handlowiec, ulica, miejscowosc])

        else:
            handlowiec = '%'
            ulica = "%"
            miejscowosc = "%"
            dom = SortAdrDomPodpisujacy.objects.raw('''SELECT lokalizacja.ID_ADR_DOM_PODPISUJACY AS id_adr_dom_podpisujacy, dane_osobowe.NAZWA_KLIENTA AS NAZWA_SPRZEDAWCY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.id_adr_dom, dom.NUMER_DOMU, symbol.SYMBOL, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(klienci.LICZBA_KLIENTOW, 0) AS LICZBA_KLIENTOW, dom.PREDKOSC_MAX, handlowiec.IMIE, handlowiec.NAZWISKO, technologie.TECHNOLOGIE FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.DANE_OSOBOWE dane_osobowe ON sprzedawca.ID_DANE_OSOBOWE = dane_osobowe.ID_DANE_OSOBOWE LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM  LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM WHERE handlowiec.nazwisko LIKE %s AND ulica.nazwa_ulicy LIKE %s AND miejscowosc.nazwa_miejscowosci LIKE %s''',[handlowiec, ulica, miejscowosc])[:0]


    hp = SortAdrDom.objects.aggregate(total_hp=Sum('licz_lokali'))
    hp2 = SortAdrDomPodpisujacy.objects.aggregate(total_dom=Count('id_adr_dom', distinct=True))

    context = {
        'dom': dom,
        'hp': hp,
        'hp2': hp2,
        'form': form,
    }
    return render(request, 'handlowiec/lokalizacje-lista.html', context)
    # return HttpResponse(hp)


def lokalizacje_json(request):
    return HttpResponse('d')