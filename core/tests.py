import django
import os
from django.core.exceptions import ObjectDoesNotExist
from MySQLdb import cursors
from django.core import serializers
from django.core.management.commands import dumpdata
from django.db import IntegrityError
from django.db.models import Sum
from django.db.transaction import rollback
from sqlparse.filters import output

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SellManager.settings")
django.setup()

from core.models import Dom, Ulica, Miejscowosc, Gmina, Powiat, Wojewodztwo, Kraj, Symbole, Budynek, Typ, Sprzedawca, \
    Handlowiec, Lokalizacja, ExternalModel, SortAdrDom, SortAdrBudynek, SortAdrTypBudynku, SortUmPodpisujacy, \
    SortAdrDomSymbol
import json

# jdata = open('../templates/modul_sprzedazy.json', 'rb')
# data = json.load(jdata)
#
# # for item in data['lokalizacje']:
# #     print(item)
#
# # def is_json(myjson):
# #   try:
# #     json_object = json.load(myjson)
# #   except ValueError as e:
# #     return False
# #   return True
# #
# # print(is_json(jdata))
# #
# # for item in data:
# #     try:
# #         kraj = item['dom']['ulica']['miejscowosc']['gmina']['powiat']['wojewodztwo']['kraj']
# #         wojewodztwo = item['dom']['ulica']['miejscowosc']['gmina']['powiat']['wojewodztwo']
# #         powiat = item['dom']['ulica']['miejscowosc']['gmina']['powiat']
# #         gmina = item['dom']['ulica']['miejscowosc']['gmina']
# #         miejscowosc = item['dom']['ulica']['miejscowosc']
# #         symbole = item['dom']['symbole']
# #         budynek = item['dom']['budynek']
# #         data_mod = item['dom']['data_mod']
# #         data_dod = item['dom']['data_dod']
# #         panel_lokalizacji = item['panel_lokalizacji']
# #
# #     except KeyError:
# #         pass
#     # print(item['dom']['technologie'])
#     # print(item['dom']['technologie']['id_gniazdka_technologie'])
#     # for field in item['dom']['technologie']:
#     #     print(field['id_gniazdka_technologie'])
#
#     # try:
#     #     if Kraj.objects.filter(id_adr_kraj=kraj['id_adr_kraj']).exists():
#     #         object_kraj = Kraj.objects.filter(id_adr_kraj=kraj['id_adr_kraj'])
#     #         object_kraj.update(nazwa_kraju=kraj['nazwa_kraju'],
#     #                            )
#     #     else:
#     #         Kraj.objects.create(id_adr_kraj=kraj['id_adr_kraj'],
#     #                             nazwa_kraju=kraj['nazwa_kraju'],
#     #                             )
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Wojewodztwo.objects.filter(id_adr_wojewodztwo=wojewodztwo['id_adr_wojewodztwo']).exists():
#     #         object_wojewodztwo = Wojewodztwo.objects.filter(id_adr_wojewodztwo=wojewodztwo['id_adr_wojewodztwo'])
#     #         object_wojewodztwo.update(id_adr_kraj=Kraj.objects.get(id_adr_kraj=wojewodztwo['id_adr_kraj']),
#     #                                   nazwa_wojewodztwa=wojewodztwo['nazwa_wojewodztwa'],
#     #                                   nr_terytu=wojewodztwo['nr_terytu']
#     #                                   )
#     #     else:
#     #         Wojewodztwo.objects.create(id_adr_wojewodztwo=wojewodztwo['id_adr_wojewodztwo'],
#     #                                    id_adr_kraj=Kraj.objects.get(id_adr_kraj=wojewodztwo['id_adr_kraj']),
#     #                                    nazwa_wojewodztwa=wojewodztwo['nazwa_wojewodztwa'],
#     #                                    nr_terytu=wojewodztwo['nr_terytu']
#     #                                    )
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Powiat.objects.filter(id_adr_powiat=powiat['id_adr_powiat']).exists():
#     #         object_powiat = Powiat.objects.filter(id_adr_powiat=powiat['id_adr_powiat'])
#     #         object_powiat.update(id_adr_wojewodztwo=Wojewodztwo.objects.get(
#     #             id_adr_wojewodztwo=powiat['id_adr_wojewodztwo']),
#     #             nazwa_powiatu=powiat['nazwa_powiatu'],
#     #             nazdod=powiat['nazdod'],
#     #             nr_terytu=powiat['nr_terytu']
#     #         )
#     #     else:
#     #         Powiat.objects.create(id_adr_powiat=powiat['id_adr_powiat'],
#     #                               id_adr_wojewodztwo=Wojewodztwo.objects.get(
#     #                                   id_adr_wojewodztwo=powiat['id_adr_wojewodztwo']),
#     #                               nazwa_powiatu=powiat['nazwa_powiatu'],
#     #                               nazdod=powiat['nazdod'],
#     #                               nr_terytu=powiat['nr_terytu']
#     #                               )
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Gmina.objects.filter(id_adr_gmina=gmina['id_adr_gmina']).exists():
#     #         object_gmina = Gmina.objects.filter(id_adr_gmina=gmina['id_adr_gmina'])
#     #         object_gmina.update(id_adr_powiat=Powiat.objects.get(id_adr_powiat=gmina['id_adr_powiat']),
#     #                             nazwa_gminy=gmina['nazwa_gminy'],
#     #                             nazdod=gmina['nazdod'],
#     #                             nr_terytu=gmina['nr_terytu']
#     #                             )
#     #     else:
#     #         Gmina.objects.create(id_adr_gmina=gmina['id_adr_gmina'],
#     #                              id_adr_powiat=Powiat.objects.get(id_adr_powiat=gmina['id_adr_powiat']),
#     #                              nazwa_gminy=gmina['nazwa_gminy'],
#     #                              nazdod=gmina['nazdod'],
#     #                              nr_terytu=gmina['nr_terytu']
#     #                              )
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Miejscowosc.objects.filter(id_adr_miejscowosc=miejscowosc['id_adr_miejscowosc']).exists():
#     #         object_miejscowosc = Miejscowosc.objects.filter(id_adr_miejscowosc=miejscowosc['id_adr_miejscowosc'])
#     #         object_miejscowosc.update(nazwa_miejscowosci=miejscowosc['nazwa_miejscowosci'],
#     #                                   id_adr_gmina=Gmina.objects.get(id_adr_gmina=miejscowosc['id_adr_gmina']),
#     #                                   nr_terytu=miejscowosc['nr_terytu'],
#     #                                   nazwa_rm=miejscowosc['nazwa_rm'])
#     #     else:
#     #         Miejscowosc.objects.create(id_adr_miejscowosc=miejscowosc['id_adr_miejscowosc'],
#     #                                    nazwa_miejscowosci=miejscowosc['nazwa_miejscowosci'],
#     #                                    id_adr_gmina=Gmina.objects.get(id_adr_gmina=miejscowosc['id_adr_gmina']),
#     #                                    nr_terytu=miejscowosc['nr_terytu'],
#     #                                    nazwa_rm=miejscowosc['nazwa_rm'])
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Ulica.objects.filter(id_adr_ulica=item['dom']['ulica']['id_adr_ulica']).exists():
#     #         object_ulica = Ulica.objects.filter(id_adr_ulica=item['dom']['ulica']['id_adr_ulica'])
#     #         object_ulica.update(id_adr_miejscowosc=Miejscowosc.objects.get(
#     #             id_adr_miejscowosc=item['dom']['ulica']['id_adr_miejscowosc']),
#     #             nazwa_ulicy_1=item['dom']['ulica']['nazwa_ulicy_1'],
#     #             nazwa_ulicy_2=item['dom']['ulica']['nazwa_ulicy_2'],
#     #             nazwa_ulicy=item['dom']['ulica']['nazwa_ulicy'],
#     #             typ=item['dom']['ulica']['typ'],
#     #             nr_terytu=item['dom']['ulica']['nr_terytu'], )
#     #
#     #     else:
#     #         Ulica.objects.create(id_adr_ulica=item['dom']['ulica']['id_adr_ulica'],
#     #                              id_adr_miejscowosc=Miejscowosc.objects.get(
#     #                                  id_adr_miejscowosc=item['dom']['ulica']['id_adr_miejscowosc']),
#     #                              nazwa_ulicy_1=item['dom']['ulica']['nazwa_ulicy_1'],
#     #                              nazwa_ulicy_2=item['dom']['ulica']['nazwa_ulicy_2'],
#     #                              nazwa_ulicy=item['dom']['ulica']['nazwa_ulicy'],
#     #                              typ=item['dom']['ulica']['typ'],
#     #                              nr_terytu=item['dom']['ulica']['nr_terytu'], )
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Dom.objects.filter(id_adr_dom=item['id_adr_dom']).exists():
#     #         object_dom = Dom.objects.filter(id_adr_dom=item['id_adr_dom'])
#     #         if item['dom']['licz_lokali'] is None or item['dom']['licz_lokali'] == '0.0':
#     #             object_dom.update(id_adr_ulica=Ulica.objects.get(id_adr_ulica=item['dom']['id_adr_ulica']),
#     #                               numer_domu=item['dom']['numer_domu'],
#     #                               # data_dod=data_dod,
#     #                               # data_mod=data_mod,
#     #                               predkosc_max=item['dom']['predkosc_max'])
#     #
#     #         else:
#     #             object_dom.update(id_adr_ulica=Ulica.objects.get(id_adr_ulica=item['dom']['id_adr_ulica']),
#     #                               numer_domu=item['dom']['numer_domu'],
#     #                               # data_dod=data_dod,
#     #                               # data_mod=data_mod,
#     #                               predkosc_max=item['dom']['predkosc_max'],
#     #                               licz_lokali=item['dom']['licz_lokali'],
#     #                               id_gniazdka_technologie=item['dom']['id_gniazdka_technologie'])
#     #
#     #     else:
#     #         Dom.objects.create(id_adr_dom=item['id_adr_dom'],
#     #                            id_adr_ulica=Ulica.objects.get(id_adr_ulica=item['dom']['id_adr_ulica']),
#     #                            numer_domu=item['dom']['numer_domu'],
#     #                            # data_dod=data_dod,
#     #                            # data_mod=data_mod,
#     #                            predkosc_max=item['dom']['predkosc_max'],
#     #                            licz_lokali=item['dom']['licz_lokali'])
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     for field in symbole:
#     #         if Symbole.objects.filter(id_adr_dom_symbol=field['id_adr_dom_symbol']).exists():
#     #             object_symbole = Symbole.objects.filter(id_adr_dom_symbol=field['id_adr_dom_symbol'])
#     #             object_symbole.update(id_adr_dom=Dom.objects.get(id_adr_dom=field['id_adr_dom']),
#     #                                   id_sprzedawca=Sprzedawca.objects.get(id_sprzedawca=field['id_sprzedawca']),
#     #                                   symbol=field['symbol'])
#     #
#     #         else:
#     #             Symbole.objects.create(id_adr_dom_symbol=field['id_adr_dom_symbol'],
#     #                                    id_adr_dom=Dom.objects.get(id_adr_dom=field['id_adr_dom']),
#     #                                    id_sprzedawca=Sprzedawca.objects.get(id_sprzedawca=field['id_sprzedawca']),
#     #                                    symbol=field['symbol'])
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Typ.objects.filter(id_adr_typ_budynku=item['dom']['budynek']['typ']['id_adr_typ_budynku']).exists():
#     #         object_typ = Typ.objects.filter(id_adr_typ_budynku=item['dom']['budynek']['typ']['id_adr_typ_budynku'])
#     #         object_typ.update(nazwa_typu=item['dom']['budynek']['typ']['nazwa_typu'])
#     #     else:
#     #         Typ.objects.create(id_adr_typ_budynku=item['dom']['budynek']['typ']['id_adr_typ_budynku'],
#     #                            nazwa_typu=item['dom']['budynek']['typ']['nazwa_typu'])
#     #
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Budynek.objects.filter(id_adr_budynek=budynek['id_adr_budynek']).exists():
#     #         object_budynek = Budynek.objects.filter(id_adr_budynek=budynek['id_adr_budynek'])
#     #         object_budynek.update(id_adr_ulica=Ulica.objects.get(id_adr_ulica=budynek['id_adr_ulica']),
#     #                               id_adr_typ_budynku=Typ.objects.get(
#     #                                   id_adr_typ_budynku=budynek['typ']['id_adr_typ_budynku']),
#     #                               numer_budynku=budynek['numer_budynku'],
#     #                               opis_budynku=budynek['opis_budynku'])
#     #     else:
#     #         Budynek.objects.create(id_adr_budynek=budynek['id_adr_budynek'],
#     #                                id_adr_ulica=Ulica.objects.get(id_adr_ulica=budynek['id_adr_ulica']),
#     #                                id_adr_typ_budynku=Typ.objects.get(
#     #                                    id_adr_typ_budynku=budynek['typ']['id_adr_typ_budynku']),
#     #                                numer_budynku=budynek['numer_budynku'],
#     #                                opis_budynku=budynek['opis_budynku'])
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Handlowiec.objects.filter(id_um_podpisujacy=panel_lokalizacji['id_um_podpisujacy']).exists():
#     #         object_handlowiec = Handlowiec.objects.filter(id_um_podpisujacy=panel_lokalizacji['id_um_podpisujacy'])
#     #         object_handlowiec.update(imie=panel_lokalizacji['imie'],
#     #                                  nazwisko=panel_lokalizacji['nazwisko'],
#     #                                  stanowisko=panel_lokalizacji['stanowisko'],
#     #                                  aktywny=panel_lokalizacji['aktywny'])
#     #     else:
#     #         Handlowiec.objects.create(id_um_podpisujacy=panel_lokalizacji['id_um_podpisujacy'],
#     #                                   imie=panel_lokalizacji['imie'],
#     #                                   nazwisko=panel_lokalizacji['nazwisko'],
#     #                                   stanowisko=panel_lokalizacji['stanowisko'],
#     #                                   aktywny=panel_lokalizacji['aktywny'])
#     # except KeyError:
#     #     pass
#     #
#     # try:
#     #     if Lokalizacja.objects.filter(id_adr_dom_podpisujacy=item['id_adr_dom_podpisujacy']).exists():
#     #         object_lokalizacja = Lokalizacja.objects.filter(id_adr_dom_podpisujacy=item['id_adr_dom_podpisujacy'])
#     #         object_lokalizacja.update(id_sprzedawca=Sprzedawca.objects.get(id_sprzedawca=item['id_sprzedawca']),
#     #                                   id_adr_dom=Dom.objects.get(id_adr_dom=item['id_adr_dom']),
#     #                                   id_um_podpisujacy=Handlowiec.objects.get(
#     #                                       id_um_podpisujacy=item['id_um_podpisujacy']),
#     #                                   )
#     #     else:
#     #         Lokalizacja.objects.create(id_adr_dom_podpisujacy=item['id_adr_dom_podpisujacy'],
#     #                                    id_sprzedawca=Sprzedawca.objects.get(id_sprzedawca=item['id_sprzedawca']),
#     #                                    id_adr_dom=Dom.objects.get(id_adr_dom=item['id_adr_dom']),
#     #                                    id_um_podpisujacy=Handlowiec.objects.get(
#     #                                        id_um_podpisujacy=item['id_um_podpisujacy']),
#     #                                    )
#     # except KeyError:
#     #     pass
#     # except Handlowiec.DoesNotExist:
#     #     Lokalizacja.objects.update_or_create(id_adr_dom_podpisujacy=item['id_adr_dom_podpisujacy'],
#     #                                id_sprzedawca=Sprzedawca.objects.get(id_sprzedawca=item['id_sprzedawca']),
#     #                                id_adr_dom=Dom.objects.get(id_adr_dom=item['id_adr_dom']),
#     #                                id_um_podpisujacy=Handlowiec.objects.get(
#     #                                    id_um_podpisujacy=250),
#     #                                )
#
# jdata.close()
#

# object_list = SortAdrDom.objects.raw(
#     "SELECT sprzedawca.ID_SPRZEDAWCA as ID, dom.ID_ADR_DOM, COUNT(DISTINCT(klient.ID_KLIENCI)) as obiekt FROM USORT4.KLIENCI klient INNER JOIN USORT4.SPRZEDAWCA sprzedawca ON klient.ID_SPRZEDAWCA = sprzedawca.ID_SPRZEDAWCA INNER JOIN USORT4.OPLATY_STALE oplata ON klient.ID_KLIENCI = oplata.ID_KLIENCI INNER JOIN USORT4.WAZNOSCI_PORTOW waznosc_portu ON oplata.ID_OPLATY_STALE = waznosc_portu.ID_OPLATY_STALE AND TRUNC(oplata.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (oplata.KON_WAZNOSCI IS NULL OR TRUNC(oplata.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) AND TRUNC(waznosc_portu.POCZ_WAZNOSCI) <= TRUNC(CURRENT_DATE) AND (waznosc_portu.KON_WAZNOSCI IS NULL OR TRUNC(waznosc_portu.KON_WAZNOSCI) >= TRUNC(CURRENT_DATE)) INNER JOIN USORT4.GNIAZDKA gniazdko ON waznosc_portu.ID_GNIAZDKA = gniazdko.ID_GNIAZDKA INNER JOIN USORT4.ADR_LOKAL lokal ON gniazdko.ID_ADR_LOKAL = lokal.ID_ADR_LOKAL INNER JOIN USORT4.ADR_DOM dom ON lokal.ID_ADR_DOM = dom.ID_ADR_DOM GROUP BY sprzedawca.ID_SPRZEDAWCA, dom.ID_ADR_DOM;")
#
#
# for p in object_list:
#     print(p.id, p.id_adr_dom, p.obiekt)


# test = SortAdrDom.objects.raw(
#     "SELECT DISTINCT USORT4.ADR_DOM.id_adr_dom, USORT4.SPRZEDAWCA.format_rekl_num, USORT4.ADR_DOM_SYMBOL.symbol, USORT4.ADR_ULICA.typ as typ_ulicy, USORT4.ADR_ULICA.nazwa_ulicy, USORT4.ADR_DOM.numer_domu, USORT4.ADR_MIEJSCOWOSC.nazwa_miejscowosci, USORT4.ADR_TYP_BUDYNKU.nazwa_typu, USORT4.ADR_DOM.licz_lokali, USORT4.ADR_DOM.predkosc_max, USORT4.um_podpisujacy.imie, USORT4.um_podpisujacy.nazwisko FROM USORT4.ADR_DOM LEFT OUTER JOIN USORT4.ADR_DOM_SYMBOL ON (USORT4.ADR_DOM.id_adr_dom = USORT4.ADR_DOM_SYMBOL.id_adr_dom) LEFT OUTER JOIN USORT4.ADR_ULICA ON (USORT4.ADR_DOM.id_adr_ulica = USORT4.ADR_ULICA.id_adr_ulica) LEFT OUTER JOIN USORT4.ADR_MIEJSCOWOSC ON (USORT4.ADR_ULICA.id_adr_miejscowosc = USORT4.ADR_MIEJSCOWOSC.id_adr_miejscowosc) LEFT OUTER JOIN USORT4.ADR_DOM_PODPISUJACY ON (USORT4.ADR_DOM.id_adr_dom = USORT4.ADR_DOM_PODPISUJACY.id_adr_dom) LEFT OUTER JOIN USORT4.UM_PODPISUJACY ON (USORT4.ADR_DOM_PODPISUJACY.id_um_podpisujacy = USORT4.um_podpisujacy.id_um_podpisujacy) LEFT OUTER JOIN USORT4.SPRZEDAWCA ON (USORT4.SPRZEDAWCA.id_sprzedawca = USORT4.ADR_DOM_PODPISUJACY.id_sprzedawca) LEFT OUTER JOIN USORT4.ADR_BUDYNEK ON (USORT4.ADR_ULICA.id_adr_ulica = USORT4.ADR_BUDYNEK.id_adr_ulica) AND (USORT4.ADR_DOM.numer_domu = USORT4.ADR_BUDYNEK.numer_budynku) LEFT OUTER JOIN USORT4.ADR_TYP_BUDYNKU ON (USORT4.ADR_BUDYNEK.id_adr_typ_budynku = USORT4.ADR_TYP_BUDYNKU.id_adr_typ_budynku)")
#
# print(test.columns)

from core.models import SortAdrDomPodpisujacy

# uruchomienie = SortAdrTypBudynku.objects.get(id_adr_typ_budynku=SortAdrBudynek.objects.get(id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=10482).id_adr_ulica, numer_budynku=SortAdrDom.objects.get(id_adr_dom=10482).numer_domu).id_adr_typ_budynku)
# .get(numer_budynku=SortAdrDom.objects.get(id_adr_dom=3457).numer_domu).id_adr_typ_budynku).nazwa_typu
try:
    typ_budynku = SortAdrTypBudynku.objects.get(id_adr_typ_budynku=SortAdrBudynek.objects.get(id_adr_ulica=SortAdrDom.objects.get(id_adr_dom=20881).id_adr_ulica, numer_budynku=SortAdrDom.objects.get(id_adr_dom=20881).numer_domu).id_adr_typ_budynku).nazwa_typu
except ObjectDoesNotExist:
    typ_budynku = "Brak"
print(typ_budynku)

# print(dom2)
#
# import cx_Oracle
# import os
# import sys
#
# print(sys.version)
# #print(os.environ['ORACLE_HOME'])
# print(os.environ['path'])
#
# con = cx_Oracle.connect('USER/pass@host:port/SID')
# print (con.version)
#
# con.close()
