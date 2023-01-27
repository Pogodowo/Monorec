from .tabela_etanolowa import tabela_etanolowa
from .models import Skladnik,Receptura
from .wspolczynniki_wyparcia import wspolczynniki_wyparcia
import sys
def Przeliczanie_etanolu(skladnik,pk,gramy):
    ret={"ilosc_etanolu":0,"ilosc_wody_do_etanolu":0}
    if skladnik=='Etanol' and gramy!='':
        oleum=Skladnik.objects.get(pk=pk)
        pozadane_stezenie=tabela_etanolowa[oleum.pozadane_stezenie]
        uzyte_stezenie=tabela_etanolowa[oleum.uzyte_stezenie]
        ilosc_etanolu_z_rec=gramy

        if ilosc_etanolu_z_rec!='':
            if float(pozadane_stezenie)<float(uzyte_stezenie):
                czysty_etanol=(float(pozadane_stezenie)/100)*float(ilosc_etanolu_z_rec)
                ilosc_etanolu=(100*float(czysty_etanol))/float(uzyte_stezenie)
                ilosc_wody=float(float(ilosc_etanolu_z_rec)-ilosc_etanolu)
                ret["ilosc_etanolu"]=str(round(ilosc_etanolu,3))
                ret["ilosc_wody_do_etanolu"] = str(round(ilosc_wody,3))
            else:
                ret["ilosc_etanolu"] = 'to_little'
                ret["ilosc_wody_do_etanolu"] = str(0)
    else:
        ret["ilosc_etanolu"] = ''
        ret["ilosc_wody_do_etanolu"] = ''


    return ret



def Sumowanie_wody(sklId,gramy_po_podziale):
   
    sys.stdout.flush()
    all = Skladnik.objects.filter(receptura_id=int(sklId))
    woda = None
    jestwoda = False

    for i in all:
        if i.skladnik == 'Woda destylowana':
            jestwoda = True
            woda = i

    if jestwoda == True and woda != None :
        t1 = [woda.ilosc_wody_do_etanolu, woda.woda_mocznik, woda.woda_kwas_borowy]
        if  woda.gramy!='' and woda.show==True:
                woda.calkowita_ilosc_gramow_wody = str(float(woda.gramy)+ float(woda.ilosc_wody_do_etanolu) + float(woda.woda_mocznik) + float(woda.woda_kwas_borowy))
                woda.save()
        else:
            a=0
            for i in t1:
                if i!='':
                    a=a+float(i)
                else:
                    pass
            woda.calkowita_ilosc_gramow_wody = str(a)
            woda.save()
        woda.save()

def Kasowanie_wody(sklId):
    all = Skladnik.objects.filter(receptura_id=int(sklId))
    woda = None
    jestwoda = False
    for i in all:
        if i.skladnik == 'Woda destylowana':
            jestwoda = True
            woda = i
    if jestwoda == True and woda != None:
        if woda.ilosc_na_recepcie == '0' and woda.ilosc_wody_do_etanolu == '0' and woda.woda_mocznik == '0' and woda.woda_kwas_borowy == '0':
            woda.delete()
            jestwoda = False
            woda = None

def Sumskl(sklId):
    all = Skladnik.objects.filter(receptura_id=int(sklId))
    last = Skladnik.objects.filter(receptura_id=int(sklId)).last()
    woda = None
    jestwoda = False
    # sprawdzanie czy receptura zawiera ad lub aa_ad##########################################
    jest_ad = False
    skladnik_z_ad = None
    jest_aa_ad = False
    skladnik_z_aa_ad = None
    for i in all:
        if i.ad == 'on':
            jest_ad = True
            skladnik_z_ad = i
        elif i.aa_ad == 'on':
            jest_aa_ad = True
            skladnik_z_aa_ad = i
        if i.skladnik == 'Woda destylowana':
            jestwoda = True
            woda = i

    a=0
    if jest_ad == True and skladnik_z_ad != None:
        for i in all:
            if i != skladnik_z_ad:
                a = a + float(i.gramy)

            if jestwoda == True and woda != None :
                if i.skladnik == 'Mocznik'  and float(i.woda_mocznik) > 0:
                    a = a + float(i.woda_mocznik)
                # if i.skladnik == 'Etanol' and skladnik_z_ad.skladnik == 'Etanol' and float(i.ilosc_wody_do_etanolu) > 0:
                #     a = a - float(i.ilosc_wody_do_etanolu)
                # if i.skladnik == '3% roztwór kwas borowy'  and i.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'on':
                #     a = a - float(i.woda_kwas_borowy)
                pass
    elif jest_aa_ad ==True and skladnik_z_aa_ad != None:
        for i in all:
            if i.gramy!=''  and i.obey!=skladnik_z_aa_ad.pk and  i.ad!='on' and i.aa_ad!='on':
                a = a+float(i.gramy)

            if jestwoda == True and woda != None :
                if i.skladnik=='Mocznik' and float(i.woda_mocznik)>0:
                    a=a+float(i.woda_mocznik)
                # if i.skladnik=='Etanol' and float(i.ilosc_wody_do_etanolu)>0:
                #     a=a-float(i.ilosc_wody_do_etanolu)
                # if i.skladnik=='3% roztwór kwas borowy' and float(i.woda_kwas_borowy)>0:
                #     a=a-float(i.woda_kwas_borowy)
                pass



    return round(a,3)


def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)



def obliczeniaOlCacVisual(sklId):
    skladniki = Skladnik.objects.filter(receptura_id=int(sklId))
    receptura = Receptura.objects.get(id=int(sklId))
    dane=[]
    for i in skladniki:
        if i.skladnik != 'Oleum Cacao':
            dane.append([i.skladnik,i.gramy,str(wspolczynniki_wyparcia[i.skladnik])])
    obl = '   Masa Oleum Cacao = ' + str(
        float(receptura.ilosc_czop_glob) * float(receptura.masa_docelowa_czop_glob)) + ' - '

    temp = 0
    obl += '('
    for i in skladniki:
        if i.skladnik != 'Oleum Cacao':
            obl = obl + i.gramy + 'g ' +  " x " + str(
                wspolczynniki_wyparcia[i.skladnik]) + ' ' +  ' + '
    obl = obl[:-3]
    obl = obl + ') = ' + str(float(receptura.ilosc_czop_glob) * float(receptura.masa_docelowa_czop_glob)) + ' - '
    obl = obl + '('
    for i in skladniki:
        if i.skladnik != 'Oleum Cacao':
            temp = temp + round(float(i.gramy) * float(wspolczynniki_wyparcia[i.skladnik]), 3)

            obl = obl + str(round(float(i.gramy) * float(wspolczynniki_wyparcia[i.skladnik]), 3)) +  ' + '
    obl = obl[:-3]
    obl = obl + ')'
    obl = obl + ' = '

    obl = obl + str(float(receptura.ilosc_czop_glob) * float(receptura.masa_docelowa_czop_glob)) + ' - ' + str(
        round(temp, 3)) + ' = ' + str(
        round(float(receptura.ilosc_czop_glob) * float(receptura.masa_docelowa_czop_glob) - temp, 3)) + 'g  '+'<br>'
    for i in skladniki:
        if i.skladnik == 'Oleum Cacao' and i.czy_powiekszyc_mase_oleum == 'off':
            pass
        elif i.skladnik == 'Oleum Cacao' and i.czy_powiekszyc_mase_oleum == 'on':
            obl = obl + str(round(float(i.gramy) - float(
                receptura.masa_docelowa_czop_glob),3)) + 'g + ' + receptura.masa_docelowa_czop_glob + 'g' + get_super(
                '(masa dodatkowego czopka/globulki)') + '= ' + i.gramy + 'g'

    return {'obliczenia': obl[3:],'dane':dane}


def obliczeniaEtVisual(sklId):# Tworzy stringi z obliczeniami etanolowymi użytymi przy tworzeniy pdf
    etanol = None
    skladniki = Skladnik.objects.filter(receptura_id=int(sklId))
    for i in skladniki:
        if i.skladnik == 'Etanol':
            etanol = i

    receptura = Receptura.objects.get(id=int(sklId))
    obl = ''
    obl1 = ''

    obl += 'Ilość potrzebnych gramów etanolu ' + etanol.pozadane_stezenie + '° t.j.' + \
           tabela_etanolowa[etanol.pozadane_stezenie] + '% wynosi ' + etanol.gramy + 'g'
    obl1 += 'Stężenie etanolu jakim dysponujeny wynosi ' + etanol.uzyte_stezenie + '° t.j. ' + \
           tabela_etanolowa[etanol.uzyte_stezenie] + '% w ujęciu wagowym'


    obl2 = ''
    obl2 += 'ilość potrzebnego etanolu ' + tabela_etanolowa[etanol.uzyte_stezenie] + '% = '
    licznik=''
    licznik =   tabela_etanolowa[etanol.pozadane_stezenie] + '  * ' + etanol.gramy
    mianownik=''
    mianownik=  tabela_etanolowa[etanol.uzyte_stezenie]
    wynik=''
    wynik= ' = ' + etanol.ilosc_etanolu + 'g'
    obl3=''
    obl3 += 'Ilość potrzebnych gramów wody wynosi  ' + etanol.gramy + ' - ' + etanol.ilosc_etanolu + ' ='  + etanol.ilosc_wody_do_etanolu + ' g '
    return {'obl': obl, 'obl1': obl1,'obl2':obl2,'licznik':licznik,'mianownik':mianownik,'wynik':wynik,'obl3':obl3}


def obliczeniaOlCacQs(last_skl,sklId,all_skl,alerty):#Oblicza masę masła kakowego w czopkach i globulkach (ref updateTable)
    if last_skl.qs == 'on' and sprawdzanie_skl_bez_gramow(all_skl)==False:
            last_skl.delete()#print(sprawdzanie_skl_bez_gramow())
    elif last_skl.qs == 'on' and sprawdzanie_skl_bez_gramow(all_skl)==True:
        receptura = Receptura.objects.get(pk=last_skl.receptura_id.pk)
        a = 0.0
        for el in all_skl:
            if el.skladnik != 'Oleum Cacao':
                a = a + float(el.gramy) * wspolczynniki_wyparcia[el.skladnik]
        last_skl.gramy = str(
            round(float(receptura.masa_docelowa_czop_glob) * float(receptura.ilosc_czop_glob) - a, 3))
        if float(last_skl.gramy)>0:
            last_skl.save()
        else:
            alerty['alert']='Masa składników przekracza docelową masę czopka/globulki'
            last_skl.delete()
    elif last_skl.ad == 'on':
        receptura = Receptura.objects.get(pk=last_skl.receptura_id.pk)
        if float(last_skl.ilosc_na_recepcie) * float(receptura.ilosc_czop_glob)>Sumskl(sklId):
            last_skl.gramy = str(round(float(last_skl.ilosc_na_recepcie) * float(receptura.ilosc_czop_glob) - Sumskl(sklId), 3))
            last_skl.save()
        else:
             alerty['alert'] = 'ilość dodanego składnika z ad musi być większa niż masa dotychczasowych skladników'
             last_skl.delete()

    if last_skl.czy_powiekszyc_mase_oleum == 'on':
        receptura = Receptura.objects.get(pk=last_skl.receptura_id.pk)
        last_skl.gramy = str(float(last_skl.gramy) + float(receptura.masa_docelowa_czop_glob))
        last_skl.save()

def sprawdzanie_skl_bez_gramow(all_skl):
    for obj in all_skl.order_by("-id")[1:]:
        if obj.gramy == '':
            return False
    return True
