from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import SortAdrDom, SortAdrDomPodpisujacy
from panel_lokalizacji.forms import SearchForm


@login_required
def lokalizacje_list(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if request.user.groups.filter(name='Handlowcy'):
                handlowiec = request.user.last_name
                form.initial['handlowiec'] = request.user.last_name
            else:
                handlowiec = form.cleaned_data.get('handlowiec')
            ulica = form.cleaned_data.get('ulica')
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
            if handlowiec != 'NULL':
                if handlowiec != '':
                    handlowiec_query = " HAVING handlowiec.nazwisko LIKE '%%" + handlowiec + "%%'"
                else:
                    handlowiec_query = " HAVING (handlowiec.nazwisko LIKE '%%" + handlowiec + "%%' OR handlowiec.nazwisko IS NULL)"
            else:
                handlowiec_query = " HAVING handlowiec.nazwisko IS NULL"
            if ulica != '':
                ulica_query = " AND ulica.nazwa_ulicy LIKE '%%" + ulica + "%%'"
            else:
                ulica_query = ""

            if miejscowosc != '':
                miejscowosc_query = " AND miejscowosc.nazwa_miejscowosci LIKE '%%" + miejscowosc + "%%'"
            else:
                miejscowosc_query = ""
            if symbol != '':
                symbol_query = " AND MIN(symbol.SYMBOL) LIKE '" + symbol + "'"
            else:
                symbol_query = ""

            if predkosc_max_od is not None or predkosc_max_do is not None:
                if predkosc_max_od is not None and predkosc_max_do is None:
                    predkosc_query = " AND dom.predkosc_max >= '" + str(predkosc_max_od) + "' "
                if predkosc_max_od is None and predkosc_max_do is not None:
                    predkosc_query = " AND dom.predkosc_max <= '" + str(predkosc_max_do) + "' "
                if predkosc_max_od is not None and predkosc_max_do is not None:
                    predkosc_query = " AND dom.predkosc_max BETWEEN '" + str(predkosc_max_od) + "' AND '" + str(
                        predkosc_max_do) + "' "
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
            liczba_klientow = 'COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0)'
            if liczba_klientow_od is not None or liczba_klientow_do is not None:
                if liczba_klientow_od == 0 and liczba_klientow_do == 0:
                    liczba_klientow_query = " AND " + liczba_klientow + " IS NULL"
                else:
                    if liczba_klientow_od is not None and liczba_klientow_do is None:
                        liczba_klientow_query = " AND " + liczba_klientow + " >= '" + str(liczba_klientow_od) + "' "
                    if liczba_klientow_od is None and liczba_klientow_do is not None:
                        liczba_klientow_query = " AND (" + liczba_klientow + " <= '" + str(
                            liczba_klientow_do) + "' OR " + liczba_klientow + " IS NULL) "
                    if liczba_klientow_od is not None and liczba_klientow_do is not None and liczba_klientow_od != 0 and liczba_klientow_do != 0:
                        liczba_klientow_query = " AND " + liczba_klientow + " BETWEEN '" + str(
                            liczba_klientow_od) + "' AND '" + str(liczba_klientow_do) + "' "
                    if liczba_klientow_od == 0 and liczba_klientow_do != 0 and liczba_klientow_do is not None:
                        liczba_klientow_query = " AND (" + liczba_klientow + " IS NULL OR " + liczba_klientow + " <= '" + str(
                            liczba_klientow_do) + "')"
                    if liczba_klientow_od == 0 and liczba_klientow_do is None:
                        liczba_klientow_query = ""
                    if liczba_klientow_od != 0 and liczba_klientow_do == 0:
                        liczba_klientow_query = " AND " + liczba_klientow + " IS NULL"
                    if liczba_klientow_od and liczba_klientow_do == 0:
                        liczba_klientow_query = " AND " + liczba_klientow + " IS NULL"
            else:
                liczba_klientow_query = ""

            wypelnienie = 'dom.LICZ_LOKALI IS NOT NULL AND dom.LICZ_LOKALI <> 0 AND ROUND((100.0 * COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0)) / (1.0 * dom.LICZ_LOKALI))'
            if wypelnienie_od is not None or wypelnienie_do is not None:
                if wypelnienie_od == 0 and wypelnienie_do == 0:
                    wypelnienie_query = " AND" + wypelnienie + "IS NULL"
                else:
                    if wypelnienie_od is not None and wypelnienie_do is None:
                        wypelnienie_query = " AND " + wypelnienie + " >= '" + str(wypelnienie_od) + "' "
                    if wypelnienie_od is None and wypelnienie_do is not None:
                        wypelnienie_query = " AND (" + wypelnienie + " <= '" + str(
                            wypelnienie_do) + "' OR " + wypelnienie + " IS NULL) "
                    if wypelnienie_od is not None and wypelnienie_do is not None and wypelnienie_od != 0 and wypelnienie_do != 0:
                        wypelnienie_query = " AND " + wypelnienie + " BETWEEN '" + str(
                            wypelnienie_od) + "' AND '" + str(wypelnienie_do) + "' "
                    if wypelnienie_od == 0 and wypelnienie_do != 0 and wypelnienie_do is not None:
                        wypelnienie_query = " AND (" + wypelnienie + " IS NULL OR " + wypelnienie + " <= '" + str(
                            wypelnienie_do) + "')"
                    if wypelnienie_od == 0 and wypelnienie_do is None:
                        wypelnienie_query = ""
                    if wypelnienie_od != 0 and wypelnienie_do == 0:
                        wypelnienie_query = " AND " + wypelnienie + "IS NULL"
                    if wypelnienie_od and wypelnienie_do == 0:
                        wypelnienie_query = " AND " + wypelnienie + " IS NULL"
            else:
                wypelnienie_query = ""

            uruchomienie = 'MIN(lokalizacja.URUCHOMIENIE)'
            if uruchomienie_od is not None or uruchomienie_do is not None:
                if uruchomienie_od is not None and uruchomienie_do is None:
                    uruchomienie_query = " AND " + uruchomienie + " >= '" + str(uruchomienie_od) + "' "
                if uruchomienie_od is None and uruchomienie_do is not None:
                    uruchomienie_query = " AND " + uruchomienie + " <= '" + str(uruchomienie_do) + "'"
                if uruchomienie_od is not None and uruchomienie_do is not None:
                    uruchomienie_query = " AND " + uruchomienie + " BETWEEN '" + str(uruchomienie_od) + "' AND '" + str(uruchomienie_do) + "' "
            else:
                uruchomienie_query = ""

            dom_sql_main = '''SELECT MIN(lokalizacja.ID_ADR_DOM_PODPISUJACY) AS id_adr_dom_podpisujacy, SUBSTR(sprzedawca.FORMAT_REKL_NUM, 5) AS NAZWA_SPRZEDAWCY, 
            gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, MIN(symbol.SYMBOL) AS SYMBOL, 
            budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0) AS LICZBA_KLIENTOW, 
            (CASE WHEN dom.LICZ_LOKALI IS NULL THEN NULL WHEN dom.LICZ_LOKALI = 0 THEN NULL ELSE ROUND((100.0 * COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0)) / (1.0 * dom.LICZ_LOKALI)) END) AS WYPELNIENIE, 
            dom.PREDKOSC_MAX, MAX(handlowiec.IMIE || ' ' || handlowiec.NAZWISKO) AS HANDLOWIEC, technologie.TECHNOLOGIE, MIN(lokalizacja.URUCHOMIENIE) AS URUCHOMIENIE 
            FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja 
            INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM 
            INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA 
            INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC 
            INNER JOIN USORT4.ADR_GMINA gmina ON miejscowosc.ID_ADR_GMINA = gmina.ID_ADR_GMINA 
            INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA 
            LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY 
            LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM 
            LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek 
            LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU 
            LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient 
            INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA 
            INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI 
            INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE
             AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL 
             OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE)
              AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) 
              INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA 
              INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL 
              INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM 
              GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA
               AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM 
               LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE 
               FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia 
               INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE 
               GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM 
               GROUP BY sprzedawca.FORMAT_REKL_NUM, gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, budynek.NAZWA_TYPU, 
               dom.LICZ_LOKALI, dom.PREDKOSC_MAX, handlowiec.nazwisko, technologie.TECHNOLOGIE'''


            dom = SortAdrDomPodpisujacy.objects.raw(dom_sql_main + handlowiec_query + ulica_query + miejscowosc_query + symbol_query + predkosc_query + hp_query + liczba_klientow_query + uruchomienie_query + wypelnienie_query)
            # return HttpResponse(dom.raw_query)
    else:
        form = SearchForm()
        if request.user.groups.filter(name='Handlowcy'):
            handlowiec = '%' + request.user.last_name + '%'
            form.initial['handlowiec'] = request.user.last_name
            ulica = "%"
            miejscowosc = "%"
            dom = SortAdrDomPodpisujacy.objects.raw('''SELECT MIN(lokalizacja.ID_ADR_DOM_PODPISUJACY) AS id_adr_dom_podpisujacy, SUBSTR(sprzedawca.FORMAT_REKL_NUM, 5) AS SYMBOL_SPRZEDAWCY, gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, MIN(symbol.SYMBOL) AS SYMBOL, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0) AS LICZBA_KLIENTOW, (CASE WHEN dom.LICZ_LOKALI IS NULL THEN NULL WHEN dom.LICZ_LOKALI = 0     THEN NULL ELSE ROUND((100.0 * COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0)) / (1.0 * dom.LICZ_LOKALI)) END) AS WYPELNIENIE, dom.PREDKOSC_MAX, MAX(handlowiec.IMIE || ' ' || handlowiec.NAZWISKO) AS HANDLOWIEC, technologie.TECHNOLOGIE, MIN(lokalizacja.URUCHOMIENIE) AS URUCHOMIENIE FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC INNER JOIN USORT4.ADR_GMINA gmina ON miejscowosc.ID_ADR_GMINA = gmina.ID_ADR_GMINA INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM GROUP BY sprzedawca.FORMAT_REKL_NUM, gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, dom.PREDKOSC_MAX, handlowiec.nazwisko, technologie.TECHNOLOGIE HAVING handlowiec.nazwisko LIKE %s AND ulica.nazwa_ulicy LIKE %s AND miejscowosc.nazwa_miejscowosci LIKE %s''', [handlowiec, ulica, miejscowosc])

        else:
            handlowiec = '%'
            ulica = "%"
            miejscowosc = "%"
            dom = SortAdrDomPodpisujacy.objects.raw(
                '''SELECT MIN(lokalizacja.ID_ADR_DOM_PODPISUJACY) AS id_adr_dom_podpisujacy, SUBSTR(sprzedawca.FORMAT_REKL_NUM, 5) AS NAZWA_SPRZEDAWCY, gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, MIN(symbol.SYMBOL) AS SYMBOL, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0) AS LICZBA_KLIENTOW, (CASE WHEN dom.LICZ_LOKALI IS NULL THEN NULL WHEN dom.LICZ_LOKALI = 0     THEN NULL ELSE ROUND((100.0 * COALESCE(SUM(klienci.LICZBA_KLIENTOW), 0)) / (1.0 * dom.LICZ_LOKALI)) END) AS WYPELNIENIE, dom.PREDKOSC_MAX, MAX(handlowiec.IMIE || ' ' || handlowiec.NAZWISKO) AS HANDLOWIEC, technologie.TECHNOLOGIE, MIN(lokalizacja.URUCHOMIENIE) AS URUCHOMIENIE FROM USORT4.ADR_DOM_PODPISUJACY lokalizacja INNER JOIN USORT4.ADR_DOM dom ON lokalizacja.ID_ADR_DOM = dom.ID_ADR_DOM INNER JOIN USORT4.ADR_ULICA ulica ON dom.ID_ADR_ULICA = ulica.ID_ADR_ULICA INNER JOIN USORT4.ADR_MIEJSCOWOSC miejscowosc ON ulica.ID_ADR_MIEJSCOWOSC = miejscowosc.ID_ADR_MIEJSCOWOSC INNER JOIN USORT4.ADR_GMINA gmina ON miejscowosc.ID_ADR_GMINA = gmina.ID_ADR_GMINA INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON lokalizacja.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA LEFT JOIN USORT4.UM_PODPISUJACY handlowiec ON lokalizacja.ID_UM_PODPISUJACY = handlowiec.ID_UM_PODPISUJACY LEFT JOIN USORT4.ADR_DOM_SYMBOL symbol ON lokalizacja.ID_SPRZEDAWCA = symbol.ID_SPRZEDAWCA AND lokalizacja.ID_ADR_DOM = symbol.ID_ADR_DOM LEFT JOIN (    SELECT budynek.ID_ADR_ULICA, budynek.NUMER_BUDYNKU, typ_budynku.NAZWA_TYPU FROM USORT4.ADR_BUDYNEK budynek LEFT JOIN USORT4.ADR_TYP_BUDYNKU typ_budynku ON budynek.ID_ADR_TYP_BUDYNKU = typ_budynku.ID_ADR_TYP_BUDYNKU) budynek ON ulica.ID_ADR_ULICA = budynek.ID_ADR_ULICA AND dom.NUMER_DOMU = budynek.NUMER_BUDYNKU LEFT JOIN (    SELECT sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) AS LICZBA_KLIENTOW FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM) klienci ON lokalizacja.ID_SPRZEDAWCA = klienci.ID_SPRZEDAWCA AND dom.ID_ADR_DOM = klienci.ID_ADR_DOM LEFT JOIN (    SELECT dom_technologia.ID_ADR_DOM, LISTAGG(technologia.NAZWA, ', ') WITHIN GROUP (ORDER BY technologia.NAZWA) AS TECHNOLOGIE FROM USORT4.ADR_DOM_TECHNOLOGIA dom_technologia INNER JOIN USORT4.GNIAZDKA_TECHNOLOGIE technologia ON dom_technologia.ID_GNIAZDKA_TECHNOLOGIE = technologia.ID_GNIAZDKA_TECHNOLOGIE GROUP BY dom_technologia.ID_ADR_DOM) technologie ON dom.ID_ADR_DOM = technologie.ID_ADR_DOM GROUP BY sprzedawca.FORMAT_REKL_NUM, gmina.NAZWA_GMINY, miejscowosc.NAZWA_MIEJSCOWOSCI, ulica.TYP, ulica.NAZWA_ULICY, dom.NUMER_DOMU, budynek.NAZWA_TYPU, dom.LICZ_LOKALI, dom.PREDKOSC_MAX, handlowiec.nazwisko, handlowiec.nazwisko,  technologie.TECHNOLOGIE HAVING handlowiec.nazwisko LIKE %s AND ulica.nazwa_ulicy LIKE %s AND miejscowosc.nazwa_miejscowosci LIKE %s''',
                [handlowiec, ulica, miejscowosc])[:0]

    sql = '''SELECT 1 as id_adr_dom, SUM("USORT4"."ADR_DOM"."LICZ_LOKALI") as total_hp 
    FROM "USORT4"."ADR_DOM" 
    WHERE "USORT4"."ADR_DOM"."ID_ADR_DOM" 
    IN (SELECT "USORT4"."ADR_DOM_PODPISUJACY"."ID_ADR_DOM" 
    FROM "USORT4"."ADR_DOM_PODPISUJACY")'''

    hp = SortAdrDom.objects.raw(sql)
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
