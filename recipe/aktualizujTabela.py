def aktualizujTabela(request, sklId):
    gramy_po_podziale = 0
    alerty = {'alert': ''}
    skl_previous_aa_ad = None
    previous_skl = None
    if len(Skladnik.objects.filter(receptura_id=int(sklId))) > 1:
        previous_skl = Skladnik.objects.filter(receptura_id=int(sklId)).order_by('-pk')[1]

    last = None
    last = Skladnik.objects.filter(receptura_id=int(sklId)).last()
    receptura = Receptura.objects.get(id=int(sklId))
    #############zamienianie ad na aa_ad jeżeli nie podano wartości w poprzednim składniku############
    if previous_skl != None and previous_skl.ilosc_na_recepcie == '' and previous_skl.show == True and last.ad == 'on':
        last.ad = 'off'
        last.aa_ad = 'on'
        last.save()
    ###########################################################################################################
    if last != None:
        if last.jednostka_z_recepty == 'gramy':
            last.gramy = last.ilosc_na_recepcie
            last.save()
        if receptura.ilosc_czop_glob != '' and last.ilosc_na_recepcie != '':
            if last.jednostka_z_recepty == 'gramy':
                last.gramy = str(round(float(last.gramy) * float(receptura.ilosc_czop_glob), 3))
                last.save()
        print('last.skladnik', last.skladnik, 'last,gramy', last.gramy, )
        g = last.gramy
        l = last.pk
        all = Skladnik.objects.filter(receptura_id=int(sklId))
        ################sprawdzanie czy jest woda i roztw kwasu borowegoi etanol i inne składniki################################
        jest_roztw_kw = False
        roztw_kw = None
        woda = None
        jestwoda = False
        etanol = None
        jestetanol = False
        mocznik = None
        jestmocznik = False
        for i in all:

            if i.skladnik == 'Woda destylowana':
                jestwoda = True
                woda = i
            elif i.skladnik == '3% roztwór kwas borowy':
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
        for i in all:
            if i.ad == 'on':
                jest_ad = True
                skladnik_z_ad = i
            elif i.aa_ad == 'on':
                jest_aa_ad = True
                skladnik_z_aa_ad = i

        ########################################################################################
        print('lastTutaj', last)
        if skladnik_z_aa_ad != None and skladnik_z_aa_ad.aa == 'on':
            skladnik_z_aa_ad.aa = 'off'
            skladnik_z_aa_ad.save()
        ###################### nowe aa################################################

        if len(all) > 1:
            ind = 0
            for el in all:
                print("el.aa = 'on'", el.aa)
                if el.aa == 'on':
                    collection = all[:ind]
                    print('collection', collection)
                    sys.stdout.flush()
                    for obj in collection[::-1]:
                        if obj.gramy == '' or obj.obey == el.pk:
                            obj.gramy = el.gramy
                            obj.obey = el.pk
                            obj.save()
                        else:
                            break
                ind = ind + 1

        ####################################################
        ########### kasowanie ilości g po usunięciu skłądnika z aa#########################
        for el in all:

            if all.filter(pk=el.obey).exists():
                pass
            else:
                if el.obey != None and el.obey != 0:
                    el.gramy = ''
                    el.obey = None
                    el.save()
        print('if jestwoda==True:2', jestwoda == True)
        if jestwoda == True:
            print('woda.gramy Tutaj', woda.gramy, 'woda.obey', woda.obey)
        ######################uwzględnianie ad#############################################
        if jest_ad == True and skladnik_z_ad != None:
            skladnik_z_ad.aa_ad_gramy = skladnik_z_ad.ilosc_na_recepcie
            skladnik_z_ad.save()
            print('skladnik_z_ad .aa_ad_gramy', skladnik_z_ad.aa_ad_gramy)
            sys.stdout.flush()
            if skladnik_z_ad.ilosc_na_recepcie == '' or float(skladnik_z_ad.ilosc_na_recepcie) < Sumskl(sklId):
                alerty['alert'] = 'ilość dodanego składnika z ad musi być większ niż masa dotychczasowych skladników'
                skladnik_z_ad.delete()
                jest_ad = False
            else:
                skladnik_z_ad.gramy = str(float(skladnik_z_ad.ilosc_na_recepcie) - Sumskl(sklId))
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

        if jest_aa_ad == True and skladnik_z_aa_ad != None:  # tutaj sprawdzam na ile składników trzeba podzielić ilość gramów z aa ad
            aa_ad_gramy = '0'
            skladnik_z_aa_ad.gramy = ''
            skladnik_z_aa_ad.save()

            for el in all.order_by('-pk'):  # order_by('-pk')
                print('el.gramy:', el.gramy, 'el.skladnik:', el.skladnik, 'el.obey!=None', el.obey != None)
                sys.stdout.flush()
                if el.ilosc_na_recepcie == '' or el.aa_ad == 'on' and el.show is True:
                    a = a + 1
                elif el.show is False:
                    pass
                else:
                    break
                print('dzelnik', a)
                sys.stdout.flush()

            reversed_list = all.order_by('-pk')
            if skladnik_z_aa_ad.ilosc_na_recepcie != '':
                # skladnik_z_aa_ad.aa_ad_gramy=skladnik_z_aa_ad.ilosc_na_recepcie#########
                skladnik_z_aa_ad.save()
                gramy_po_podziale = str(round((float(skladnik_z_aa_ad.ilosc_na_recepcie) - Sumskl(sklId)) / a, 2))
            print('gramy_po_podziale', gramy_po_podziale, 'Sumskl(sklId)', Sumskl(sklId), 'a', a)
            sys.stdout.flush()
            print(' reversed_list[0]', reversed_list[0].skladnik)
            sys.stdout.flush()
            print('a', a)
            sys.stdout.flush()
            b = 0

            while b < a:
                ob = reversed_list[b]
                if ob.show == True:
                    ob.gramy = gramy_po_podziale
                    ob.obey = skladnik_z_aa_ad.pk
                    ob.save()
                    if ob.skladnik == 'Etanol':
                        etanol.gramy = gramy_po_podziale
                        etanol.save()
                    elif ob.skladnik == '3% roztwór kwas borowy' and roztw_kw != None:
                        roztw_kw.gramy = gramy_po_podziale
                        roztw_kw.save()
                    elif ob.skladnik == 'Woda destylowana' and woda != None:
                        woda.gramy = gramy_po_podziale
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
                roztw_kw.woda_kwas_borowy = str(round(float(roztw_kw.gramy) - float(roztw_kw.gramy) * 0.03, 2))
                roztw_kw.ilosc_kwasu_borowego_do_roztworu = str(round(float(roztw_kw.gramy) * 0.03, 2))
                roztw_kw.save()
                if jestwoda == True and woda != None:
                    woda.woda_kwas_borowy = roztw_kw.woda_kwas_borowy
                    woda.save()
                elif jestwoda == False:
                    woda = Skladnik.objects.create(receptura_id=receptura, skladnik='Woda destylowana', show=False,
                                                   woda_kwas_borowy=roztw_kw.woda_kwas_borowy)
                    jestwoda = True

        ##############usuwanie kwasu bornego po usunięciu roztworu penie ten fragment do wywalenia################################
        if roztw_kw != None and roztw_kw.czy_zlozyc_roztwor_ze_skladnikow_prostych == 'off' and jestwoda == True:
            roztw_kw.woda_kwas_borowy = '0'
            roztw_kw.ilosc_kwasu_borowego_do_roztworu = '0'
            woda.woda_kwas_borowy = '0'
            roztw_kw.save()
            woda.save()

        #####################obliczenia###################################################################

        if jestetanol == True and etanol != None:
            to_updade = Przeliczanie_etanolu(etanol.skladnik, etanol.pk, etanol.gramy)
            print('etanol.gramy', etanol.gramy)
            sys.stdout.flush()
            if to_updade['ilosc_etanolu'] == 'dupa':  # jeżeli stężenie użytego jest mniejsz niż potrzebnego
                alerty[
                    'alert'] = 'Stężenie Etanolu na recepcie musi być mniejsze niż posiadanego do sporządzenia roztworu'
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

        if last.skladnik == 'Oleum Cacao':
            obiekt = Skladnik.objects.get(pk=last.pk)
            receptura = Receptura.objects.get(pk=obiekt.receptura_id.pk)
            print('receptura', receptura)
            sys.stdout.flush()
            if obiekt.qs == 'on':
                a = 0.0
                for el in all:
                    if el.skladnik != 'Oleum Cacao':
                        a = a + float(el.gramy) * wspolczynniki_wyparcia[el.skladnik]
                last.gramy = str(
                    round(float(receptura.masa_docelowa_czop_glob) * float(receptura.ilosc_czop_glob) - a, 3))
                last.save()
            elif obiekt.ad == 'on':
                last.gramy = str(
                    round(float(last.ilosc_na_recepcie) * float(receptura.ilosc_czop_glob) - Sumskl(sklId), 3))
                last.save()
            if obiekt.czy_powiekszyc_mase_oleum == 'on':
                last.gramy = str(float(last.gramy) + float(receptura.masa_docelowa_czop_glob))
                last.save()

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

    else:
        datax = {}
        parametry = serializers.serialize("python", Receptura.objects.filter(pk=int(sklId)))
        datax['slownik'] = table_dict
        datax['parametry'] = parametry[0]
        datax['objects'] = None
        datax['alerty'] = None
        # datax['wyswietlane_dane'] = wyswietlane_dane(objects)
    return JsonResponse({'tabela_zbiorcza': datax})
