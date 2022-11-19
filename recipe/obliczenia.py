from .tabela_etanolowa import tabela_etanolowa
from .models import Skladnik,Receptura
import sys
def Przeliczanie_etanolu(skladnik,pk,gramy):
    ret={"ilosc_etanolu":0,"ilosc_wody_do_etanolu":0}
    if skladnik=='Etanol' and gramy!='':
        obiekt=Skladnik.objects.get(pk=pk)
        pozadane_stezenie=tabela_etanolowa[obiekt.pozadane_stezenie]
        uzyte_stezenie=tabela_etanolowa[obiekt.uzyte_stezenie]
        ilosc_etanolu_z_rec=gramy

        if ilosc_etanolu_z_rec!='':
            if float(pozadane_stezenie)<float(uzyte_stezenie):
                czysty_etanol=(float(pozadane_stezenie)/100)*float(ilosc_etanolu_z_rec)
                ilosc_etanolu=(100*float(czysty_etanol))/float(uzyte_stezenie)
                ilosc_wody=float(float(ilosc_etanolu_z_rec)-ilosc_etanolu)
                ret["ilosc_etanolu"]=str(round(ilosc_etanolu,2))
                ret["ilosc_wody_do_etanolu"] = str(round(ilosc_wody,2))
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
        woda.gramy=0
        if  woda.gramy!='' and woda.show==True:
            a = 0
            if float(gramy_po_podziale)>0:
                woda.gramy=gramy_po_podziale
            else:
                if woda.ilosc_na_recepcie!='':
                    woda.gramy = woda.ilosc_na_recepcie
            if float(gramy_po_podziale)>0:
                    woda.calkowita_ilosc_gramow_wody = str(float(woda.gramy)+ float(woda.ilosc_wody_do_etanolu) + float(woda.woda_mocznik) + float(woda.woda_kwas_borowy))
                    woda.save()
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

