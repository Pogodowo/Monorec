from django.shortcuts import render
from django.http import JsonResponse,response
from django.shortcuts import redirect
from django.contrib.sessions.models import Session
import sys
from django.core import serializers
from .connon_fields import fields

from .models import Receptura,Skladnik,Licznik_receptur
from .lista_składników import data
from .słownik_do_tabeli import table_dict
from .obliczenia import Kasowanie_wody,Sumowanie_wody,Sumskl,get_super,Przeliczanie_etanolu,obliczeniaOlCacVisual,obliczeniaEtVisual,obliczeniaOlCacQs
from .przelWitamin import PrzeliczanieWit
from .wyswietlane_dane import wyswietlane_dane
from .tabela_etanolowa import tabela_etanolowa
from .wspolczynniki_wyparcia import wspolczynniki_wyparcia

def home (request):
    if not request.session.exists(request.session.session_key):
        request.session.create()
    return render (request,'home.html')

def dodajRecForm(request): #podaje dane potrzebne do stworzenie formularza dla nowej receptury przy użyciu ajax
    if not request.session.exists(request.session.session_key):
        request.session.create()
    context={'fields':fields}
    return JsonResponse(context)


def aktualnaRec(request):#wyświetla recepturę nad którą aktualnie pracuje użytkownik
    this_session_rec = Receptura.objects.filter(session=request.session.session_key)
    if len(this_session_rec)>0:
        actual_recipe=this_session_rec.last()
        actual_pk=actual_recipe.pk
        return redirect(f'receptura/({actual_pk})')
    else:
        return render(request,'404.html')

def dodawanieRecJson(request): #dodaję recepturę do bazy danych
    liczba_receptur=Licznik_receptur.objects.all().first()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        ilosc_receptur=0
        nazwa = request.POST.get("nazwa")
        rodzaj=request.POST.get("rodzaj")
        parametryDict={}
        parametry=fields[request.POST.get('rodzaj')]
        ###################################################################################################
        for i in parametry:
            if type(i) != list:
                parametryDict[i]=request.POST.get(i)
            else:
                a = request.POST.get(str(i[0]))
                parametryDict[i[0]] = a
        this_session_rec=Receptura.objects.filter(session=request.session.session_key)
        if len(this_session_rec)>0:
            this_session_rec.delete()
        new_skl=None
        if ilosc_receptur<2 :
            new_skl=Receptura.objects.create(rodzaj=rodzaj)
            liczba_receptur.ilosc_receptur+=1
            liczba_receptur.save()
        else:
            parametryDict['res']='przekroczona liczba'

        new_skl.session=Session.objects.get(session_key=request.session.session_key)
        if new_skl!=None:
            for key, value in parametryDict.items():
                setattr(new_skl, key, value)
            new_skl.save()
            parametryDict['id']=new_skl.id
        return JsonResponse({'dict':parametryDict})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)

def receptura (request,receptura_id):#wyświetla stronę danej receptury

    session = request.session.session_key
    try:
        receptura=Receptura.objects.get(id=receptura_id)
        if   receptura.session !=None  and receptura in Receptura.objects.filter(session=session):
            context = {'receptura': receptura}
            return render(request, 'receptura.html', context)
        else:
            return render(request, '404.html',)
    except Receptura.DoesNotExist:
        return render(request, '404.html', )

def formJson (request,skl):#odpowiada za podanie do formularza odpowiednich pól przyporządkowanych do danego składnika
    #skl zawiera tutaj nazwę składnika i id receptury
    ind=skl.index('&')
    formData={}
    datadict=data[skl[:ind]]
    all_skl =Skladnik.objects.filter(receptura_id=int(skl[ind+1:]))

    # sprawdzanie czy receptura zawiera ad lub aa_ad##########################################
    jest_ad = False
    skladnik_z_ad = None
    jest_aa_ad = False
    skladnik_z_aa_ad = None
    jest_qs = False
    skladnik_z_qs = None
    for i in all_skl:
        if i.ad == 'on':
            jest_ad = True
            skladnik_z_ad = i
        elif i.aa_ad == 'on':
            jest_aa_ad = True
            skladnik_z_aa_ad = i
        elif i.qs == 'on':
            jest_qs = True
            skladnik_z_qs = i
    ############# kończenie receptury jeżeli zawiera składnik z ad lun aa ad ####################################
    if  (skladnik_z_ad!= None and jest_ad ==True) or (skladnik_z_aa_ad!= None and jest_aa_ad ==True)or (skladnik_z_qs!= None and jest_qs ==True):
            datadict=['receptura zakończona. Ostatni skladnik zawiera ad lub aa ad. Aby konynuować musisz usunąć bądź edytować ostatni skladnik ']


    for i in all_skl:
        if i.skladnik ==skl[:ind] and i.show==True:
            datadict=['ten składnik już został dodany']

    formData['datadict']=datadict
    formData['table_dict']=table_dict
    #context = {'datadict': datadict}
    context={ 'formData':formData}
    return JsonResponse(context)

def dodajsklJson (request,sklId):
    if  request.headers.get('x-requested-with') == 'XMLHttpRequest':
        previous_skl = Skladnik.objects.filter(receptura_id=int(sklId)).last()
        new_skl=None
        dodanySkladnik=request.POST.get("skladnik")
        receptura=Receptura.objects.get(id=int(sklId))
        ilosc=request.POST.get("ilosc_na_recepcie")
        all_skl = Skladnik.objects.filter(receptura_id=int(sklId))
        to_updade={}
        if len(all_skl)<11:
            ###########sprawdzanie czy jest woda################
            woda=None
            jestwoda = False
            for i in all_skl:
                if i.skladnik == 'Woda destylowana':
                    jestwoda = True
                    woda = i
            mocznik = None
            jestmocznik = False
            for i in all_skl:
                if i.skladnik == 'Mocznik':
                    jestmocznik = True
                    mocznik = i

            ################################################################################
            if dodanySkladnik=='Woda destylowana':
                if jestwoda==False:
                    new_skl = Skladnik.objects.create(skladnik=dodanySkladnik, receptura_id=receptura,
                                                      ilosc_na_recepcie=ilosc)
                    jestwoda=True
                else:
                    woda.delete()
                    new_skl = Skladnik.objects.create(skladnik=dodanySkladnik, receptura_id=receptura,
                                                      ilosc_na_recepcie=ilosc)

            else:
                new_skl=Skladnik.objects.create(skladnik=dodanySkladnik,receptura_id=receptura,ilosc_na_recepcie=ilosc,)

            if new_skl!=None:
                to_updade={'skladnik' :new_skl.skladnik, 'jednostka_z_recepty':new_skl.jednostka_z_recepty}
                for i in data[dodanySkladnik]:
                    if type(i)!=list:
                        a=request.POST.get(str(i))
                        to_updade[i]=a
                    else:
                        a = request.POST.get(str(i[0]))
                        to_updade[i[0]] = a

                #==========wstawianie gramów==========================
                if to_updade['jednostka_z_recepty']=='gramy':
                    to_updade['gramy']=ilosc
                if receptura.ilosc_czop_glob!='' and new_skl.ilosc_na_recepcie!='':
                    if to_updade['jednostka_z_recepty']=='gramy':
                        to_updade['gramy']=str(round(float(ilosc)*float(receptura.ilosc_czop_glob),3))
                #do wywalenia jak popraeię obliczenia witamin
                    elif to_updade['jednostka_z_recepty']=='solutio':
                        to_updade['gramy']=str(round(float(ilosc)*float(receptura.ilosc_czop_glob),3))

                #=====================================================
                if 'aa_ad' in to_updade:
                    if to_updade['aa_ad']=='on':
                        to_updade['aa_ad_gramy']=ilosc

                #=================przelicanie witamin======================================
                if new_skl.skladnik in ['Witamina A','Witamina E','Oleum Menthae piperitae','Nystatyna','Mocznik' ] and to_updade['ilosc_na_recepcie']!='' :
                   to_updade=PrzeliczanieWit(dodanySkladnik,to_updade,receptura.rodzaj,receptura.ilosc_czop_glob)

                for key, value in to_updade.items():
                    setattr(new_skl, key, value)
                new_skl.save()
                ####################dodawanie aut aa bo w uptade Table trzeba było odświerzać to dodaję tu
                print("new_skl.ilosc_na_recepcie.isnumeric()",new_skl.ilosc_na_recepcie.isnumeric() )
                if previous_skl != None and previous_skl.gramy == '' and new_skl.gramy != '' :#and new_skl.ilosc_na_recepcie.isnumeric()
                    new_skl.aa = 'on'
                    new_skl.save()
                #############zamienianie ad na aa_ad jeżeli nie podano wartości w poprzednim składniku############
                if previous_skl!=None and previous_skl.ilosc_na_recepcie == '' and previous_skl.show==True and new_skl.ad=='on':
                    new_skl.ad='off'
                    new_skl.aa_ad='on'
                    new_skl.save()

        else:
            to_updade['za_duzo_skladnikow']='za_duzo_skladnikow'

        return JsonResponse({'tabela':to_updade})
    return JsonResponse({'nie dodano skladnika': False, }, safe=False)



def aktualizujTabela(request, sklId):
    gramy_po_podziale = 0
    alerty = {'alert': ''}
    previous_skl = None
    if len(Skladnik.objects.filter(receptura_id=int(sklId))) > 1:
        previous_skl = Skladnik.objects.filter(receptura_id=int(sklId)).order_by('-pk')[1]

    last_skl = None
    last_skl = Skladnik.objects.filter(receptura_id=int(sklId)).last()
    receptura = Receptura.objects.get(id=int(sklId))
    #############zamienianie ad na aa_ad jeżeli nie podano wartości w poprzednim składniku############
    if previous_skl != None and previous_skl.ilosc_na_recepcie == '' and previous_skl.show == True and last_skl.ad == 'on':
        last_skl.ad = 'off'
        last_skl.aa_ad = 'on'
        last_skl.save()
    ###########################################################################################################
    if last_skl != None:
        if last_skl.jednostka_z_recepty == 'gramy':
            last_skl.gramy = last_skl.ilosc_na_recepcie
            last_skl.save()
        if receptura.ilosc_czop_glob != '' and last_skl.ilosc_na_recepcie != '':
            if last_skl.jednostka_z_recepty == 'gramy':
                last_skl.gramy = str(round(float(last_skl.gramy) * float(receptura.ilosc_czop_glob), 3))
                last_skl.save()

        all_skl = Skladnik.objects.filter(receptura_id=int(sklId))
        ################sprawdzanie czy jest woda i roztw kwasu borowegoi etanol i inne składniki################################
        jest_roztw_kw = False
        roztw_kw = None
        woda = None
        jestwoda = False
        etanol = None
        jestetanol = False
        mocznik = None
        jestmocznik = False
        for i in all_skl:

            if i.skladnik == 'Woda destylowana':
                jestwoda = True
                woda = i
            elif i.skladnik == '3% roztwór kwasu borowego':
                jest_roztw_kw = True
                roztw_kw = i
            elif i.skladnik == 'Etanol':
                jestetanol = True
                etanol = i
            elif i.skladnik == 'Mocznik':
                jestmocznik = True
                mocznik = i
            ####################k
            # sprawdzanie czy receptura zawiera ad lub aa_ad##########################################
        jest_ad = False
        skladnik_z_ad = None
        jest_aa_ad = False
        skladnik_z_aa_ad = None
        for i in all_skl:
            if i.ad == 'on':
                jest_ad = True
                skladnik_z_ad = i
            elif i.aa_ad == 'on':
                jest_aa_ad = True
                skladnik_z_aa_ad = i

        ########################################################################################
        if skladnik_z_aa_ad != None and skladnik_z_aa_ad.aa == 'on':
            skladnik_z_aa_ad.aa = 'off'
            skladnik_z_aa_ad.save()
        ###################### nowe aa################################################

        if len(all_skl) > 1:
            ind = 0
            for el in all_skl:
                if el.aa == 'on':
                    collection = all_skl[:ind]
                    for obj in collection[::-1]:
                        if obj.gramy == '' or obj.obey == el.pk:
                            obj.gramy = el.gramy
                            obj.obey = el.pk
                            obj.save()
                        else:
                            break
                ind = ind + 1


        ########### kasowanie ilości g po usunięciu skłądnika z aa#########################
        for el in all_skl:

            if all_skl.filter(pk=el.obey).exists():
                pass
            else:
                if el.obey != None and el.obey != 0:
                    el.gramy = ''
                    el.obey = None
                    el.save()


        ######################uwzględnianie ad#############################################
        if jest_ad == True and skladnik_z_ad != None:
            skladnik_z_ad.aa_ad_gramy = skladnik_z_ad.ilosc_na_recepcie
            skladnik_z_ad.save()
            if (skladnik_z_ad.ilosc_na_recepcie == '' or float(skladnik_z_ad.ilosc_na_recepcie) < Sumskl(sklId)) and skladnik_z_ad.skladnik!='Oleum Cacao':
                alerty['alert'] = 'ilość dodanego składnika z ad musi być większa niż masa dotychczasowych skladników'
                skladnik_z_ad.delete()
                jest_ad = False
            else:
                skladnik_z_ad.gramy = str(round(float(skladnik_z_ad.ilosc_na_recepcie) - Sumskl(sklId),3))
                gramy_po_podziale = skladnik_z_ad.gramy
                skladnik_z_ad.save()
        elif jest_ad == True and skladnik_z_ad != None and skladnik_z_ad.ad == 'on' and skladnik_z_ad.aa == 'on':
            skladnik_z_ad.aa_ad = 'on'
            skladnik_z_ad.aa = 'off'
            skladnik_z_ad.ad = 'off'
            jest_ad = False
            jest_aa_ad = True
            skladnik_z_aa_ad = skladnik_z_ad
            skladnik_z_ad.aa_ad_gramy = skladnik_z_ad.ilosc_na_recepcie
            skladnik_z_ad.save()

        ################uwzględnianie aa ad#####################################################

        a = 0
        print('Sumskl(sklId)',Sumskl(sklId))
        if jest_aa_ad == True and skladnik_z_aa_ad != None:  # tutaj sprawdzam na ile składników trzeba podzielić ilość gramów z aa ad
            aa_ad_gramy = '0'
            skladnik_z_aa_ad.gramy = ''
            skladnik_z_aa_ad.save()

            for el in all_skl.order_by('-pk'):  # order_by('-pk')

                if el.ilosc_na_recepcie == '' or el.aa_ad == 'on' and el.show is True:
                    a = a + 1
                elif el.show is False:
                    pass
                else:
                    break

            reversed_list = all_skl.order_by('-pk')
            if skladnik_z_aa_ad.ilosc_na_recepcie != '':
                # skladnik_z_aa_ad.aa_ad_gramy=skladnik_z_aa_ad.ilosc_na_recepcie#########
                skladnik_z_aa_ad.save()
                gramy_po_podziale = str(round((float(skladnik_z_aa_ad.ilosc_na_recepcie) - Sumskl(sklId)) / a, 3))

            b = 0

            while b < a:
                ob = reversed_list[b]
                if ob.show == True:
                    print('skladnik',ob.skladnik)

                    ob.gramy = gramy_po_podziale
                    ob.obey = skladnik_z_aa_ad.pk
                    ob.save()
                    if ob.skladnik == 'Etanol':
                        etanol.gramy = gramy_po_podziale
                        etanol.save()
                    elif ob.skladnik == '3% roztwór kwasu borowego' and roztw_kw != None:
                        roztw_kw.gramy = gramy_po_podziale
                        roztw_kw.save()
                    elif ob.skladnik == 'Woda destylowana' and woda != None:
                        woda.gramy = gramy_po_podziale
                        woda.obey = skladnik_z_aa_ad.pk# test
                        woda.save()
                    b = b + 1
                elif ob.show is False:
                    b = b + 1
                    a = a + 1
                else:
                    b = b + 1

        #########################uwzględnianie mocznika i wody##############################
        receptura = Receptura.objects.get(id=int(sklId))

        if jestmocznik == True and mocznik.dodaj_wode == 'on':
            mocznik.woda_mocznik = str(float(mocznik.ilosc_na_recepcie) * 1.5)
            mocznik.save()
            if jestwoda == True:
                woda.woda_mocznik = str(float(mocznik.ilosc_na_recepcie) * 1.5)
                woda.save()
            elif jestwoda == False:
                Skladnik.objects.create(receptura_id=receptura, skladnik='Woda destylowana', show=False,
                                        woda_mocznik=mocznik.woda_mocznik)
                Sumowanie_wody(sklId, None)
                jestwoda = True
        Kasowanie_wody(sklId)

        #########################komponowanie roztworu kwasu bornego z kwasu i wody##############################
        if jest_roztw_kw != False and roztw_kw != None and (roztw_kw.gramy == '' or roztw_kw.gramy == '0'):
            if roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'on':
                roztw_kw.woda_kwas_borowy = '0'
                roztw_kw.ilosc_kwasu_borowego_do_roztworu = '0'
                roztw_kw.save()
        if jest_roztw_kw != False and roztw_kw != None and roztw_kw.gramy != '':
            if roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'on':
                roztw_kw.woda_kwas_borowy = str(round(float(roztw_kw.gramy) - float(roztw_kw.gramy) * 0.03, 3))
                roztw_kw.ilosc_kwasu_borowego_do_roztworu = str(round(float(roztw_kw.gramy) * 0.03, 3))
                roztw_kw.save()
                if jestwoda == True and woda != None:
                    woda.woda_kwas_borowy = roztw_kw.woda_kwas_borowy
                    woda.save()
                elif jestwoda == False:
                    woda = Skladnik.objects.create(receptura_id=receptura, skladnik='Woda destylowana', show=False,
                                                   woda_kwas_borowy=roztw_kw.woda_kwas_borowy)
                    jestwoda = True

        ##############usuwanie kwasu bornego po usunięciu roztworu ################################
        if roztw_kw != None and roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'off' and jestwoda == True:
            roztw_kw.woda_kwas_borowy = '0'
            roztw_kw.ilosc_kwasu_borowego_do_roztworu = '0'
            woda.woda_kwas_borowy = '0'
            roztw_kw.save()
            woda.save()

        #####################obliczenia###################################################################

        if jestetanol == True and etanol != None:
            to_updade = Przeliczanie_etanolu(etanol.skladnik, etanol.pk, etanol.gramy)

            if to_updade['ilosc_etanolu'] == 'to_little':  # jeżeli stężenie użytego jest mniejsz niż potrzebnego
                alerty['alert'] = 'Stężenie Etanolu na recepcie musi być mniejsze niż posiadanego do sporządzenia roztworu'
                etanol.delete()
                jestetanol = False
            else:
                etanol.ilosc_etanolu = to_updade["ilosc_etanolu"]
                etanol.ilosc_wody_do_etanolu = to_updade["ilosc_wody_do_etanolu"]
                etanol.save()

            if jestwoda == True and woda != None:
                woda.ilosc_wody_do_etanolu = etanol.ilosc_wody_do_etanolu
                woda.save()

            elif jestwoda == False:
                woda = Skladnik.objects.create(receptura_id=receptura, skladnik='Woda destylowana', show=False,
                                               ilosc_wody_do_etanolu=etanol.ilosc_wody_do_etanolu)
                jestwoda = True
            etanol.save()

        if jestetanol == False and jestwoda == True and woda != None:
            woda.ilosc_wody_do_etanolu = '0'

        if last_skl.skladnik == 'Oleum Cacao':#obliczanie ilości masła kakowego
            obliczeniaOlCacQs(last_skl,sklId,all_skl,alerty)

        Sumowanie_wody(sklId, gramy_po_podziale)
        Kasowanie_wody(sklId)
        objects = serializers.serialize("python", Skladnik.objects.filter(receptura_id=int(sklId)))
        parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(sklId)))
        datax = {}
        datax['slownik'] = table_dict
        datax['parametry'] = parametry[0]
        datax['objects'] = objects
        datax['alerty'] = alerty
        datax['wyswietlane_dane'] = wyswietlane_dane(objects)
        datax['wspolczynniki_wyparcia']=wspolczynniki_wyparcia

    else:
        datax = {}
        parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(sklId)))
        datax['slownik'] = table_dict
        datax['parametry'] = parametry[0]
        datax['objects'] = None
        datax['alerty'] = None
        # datax['wyswietlane_dane'] = wyswietlane_dane(objects)
    return JsonResponse({'tabela_zbiorcza': datax})


def delSkl(request, id):
    deletedElement = Skladnik.objects.filter(pk=id)

    skl = Skladnik.objects.get(pk=id)
    all_skl = Skladnik.objects.filter(receptura_id=skl.receptura_id)
    ################sprawdzanie czy jest woda ################################
    woda = None
    jestwoda = False
    for i in all_skl:
        if i.skladnik == 'Woda destylowana':
            jestwoda = True
            woda = i
    ########################################################################################
    if skl.skladnik == 'Mocznik':
        if jestwoda == True and woda:
            woda.woda_mocznik = '0'
            woda.save()
    if skl.skladnik == 'Etanol':
        if jestwoda == True and woda:
            woda.ilosc_wody_do_etanolu = '0'
            woda.save()
    if skl.skladnik == '3% roztwór kwasu borowego':
        if jestwoda == True and woda:
            woda.woda_kwas_borowy = '0'
            woda.save()

    ####################################################################
    Kasowanie_wody(id)
    Sumowanie_wody(id, None)
    ####################################################################
    response = serializers.serialize("python", deletedElement)
    deletedElement.delete()

    return JsonResponse({'response': response})


def editFormJson(request, skl):
    receptura_id = Skladnik.objects.get(pk=int(skl)).receptura_id
    lastEdit = Skladnik.objects.filter(receptura_id=(receptura_id)).last().skladnik
    skladnik = Skladnik.objects.get(pk=int(skl)).skladnik
    show= Skladnik.objects.get(pk=int(skl)).show
    skladnik_obj = Skladnik.objects.get(pk=int(skl))
    datadict = {'form': data[skladnik], 'values': {}}
    lista_el_do_edycji = []

    if skladnik != lastEdit and show == True:
        for i in data[skladnik]:
            if i not in ['aa', 'ad', 'aa_ad', 'qs', 'dodaj_wode', 'czy_zlozyc_roztwor_ze_skladnikow_prostych']:
                lista_el_do_edycji.append(i)
    elif show == False:#uniemożliwia edycję automatycznie dodanego składnika
         pass
    else:
        lista_el_do_edycji = data[skladnik]

    datadict['form'] = lista_el_do_edycji

    for j in lista_el_do_edycji:
        if type(j) == list:
            j = j[0]
            datadict['values'][str(j)] = getattr(skladnik_obj, j)
        else:
            datadict['values'][str(j)] = getattr(skladnik_obj, j)
    context = {'datadict': datadict, 'slownik': table_dict}
    return JsonResponse(context)


def edytujsklJson(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        nazwa_skladnika = request.POST.get("skladnik")
        ilosc = request.POST.get("ilosc_na_recepcie")
        edytowany_skladnik = Skladnik.objects.get(pk=int(pk))
        receptura = Receptura.objects.get(pk=edytowany_skladnik.receptura_id.pk)
        to_edit = {'skladnik': nazwa_skladnika, 'jednostka_z_recepty': edytowany_skladnik.jednostka_z_recepty}
        for j in data[nazwa_skladnika]:
            if type(j) != list:
                if str(j) in request.POST:
                    a = request.POST.get(str(j))
                    to_edit[j] = a
                else:
                    pass
            else:
                if str(j[0]) in request.POST:
                    a = request.POST.get(str(j[0]))
                    to_edit[j[0]] = a
                else:
                    pass

            # ==========wstawianie gramów==========================
        if to_edit['jednostka_z_recepty'] == 'gramy':
            to_edit['gramy'] = ilosc

        if receptura.rodzaj == 'czopki_i_globulki' and to_edit['ilosc_na_recepcie'] != '':
            to_edit[to_edit['jednostka_z_recepty']] = str(round(
                float(to_edit['ilosc_na_recepcie']) * float(receptura.ilosc_czop_glob), 3))
        # =====================================================
        if 'aa_ad' in to_edit:
            to_edit['aa_ad_gramy'] = to_edit['gramy']

        if to_edit['skladnik'] == 'Witamina A' or to_edit['skladnik'] == 'Witamina E' or to_edit[
            'skladnik'] == 'Oleum Menthae piperitae' or to_edit['skladnik'] == 'Nystatyna':
            to_edit = PrzeliczanieWit(to_edit['skladnik'], to_edit, receptura.rodzaj, receptura.ilosc_czop_glob)

        for key, value in to_edit.items():
            setattr(edytowany_skladnik, key, value)
        edytowany_skladnik.save()
        return JsonResponse({'tabela': to_edit})

    return JsonResponse({'nie dodano skladnika': False, }, safe=False)


def slownikJson(request):
    # response = serializers.serialize("python", deletedElement)
    return JsonResponse({'table_dict': table_dict})






def obliczeniaOlCacJson(request, sklId):
   data=obliczeniaOlCacVisual(sklId)
   return JsonResponse(data)



def obliczeniaEtJson(request, sklId):
    etanol = None
    skladniki = Skladnik.objects.filter(receptura_id=int(sklId))
    for i in skladniki:
        if i.skladnik == 'Etanol':
            etanol = i

    receptura = Receptura.objects.get(id=int(sklId))
    obl = ''

    obl += '\\[\\begin{flalign}Ilość\;potrzebnych\;gramów\;etanolu \;' + etanol.pozadane_stezenie + '° \;(\;t.j.\;' + \
           tabela_etanolowa[etanol.pozadane_stezenie] + '\%\;)\; wynosi \;' + etanol.gramy + 'g\\end{flalign}\\]'
    obl += '\\[\\begin{flalign}&Stężenie\;etanolu\;jakim\;dysponujeny\;wynosi\;' + etanol.uzyte_stezenie + '° t.j.\; ' + \
           tabela_etanolowa[etanol.uzyte_stezenie] + '\%\; w\;ujęciu\;wagowym' + '\\end{flalign}\\]'

    # obl="$$\\begin{aligned} 2x - 4 &= 6 \\\\ 2x &= 10 \\\\ x &= 5 \end{aligned}$$"
    obl1 = ''
    obl1 += '\\[{ilość\;potrzebnego\;etanolu\; ' + tabela_etanolowa[etanol.uzyte_stezenie] + '\% } = {\LARGE' + \
            tabela_etanolowa[etanol.pozadane_stezenie] + '  * ' + etanol.gramy + '\\over\Large' + tabela_etanolowa[
                etanol.uzyte_stezenie] + '}={' + etanol.ilosc_etanolu + '\;g }\\]'
    obl1 += '\\[\\begin{flalign}Ilość\;potrzebnych\;gramów\;wody\;wynosi:\; \; ' + etanol.gramy + '-' + etanol.ilosc_etanolu + '=' + etanol.ilosc_wody_do_etanolu + '\; g\\end{flalign}\\]'
    return JsonResponse({'tabela': {'obl': obl, 'obl1': obl1}})