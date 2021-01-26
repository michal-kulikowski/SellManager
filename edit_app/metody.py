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