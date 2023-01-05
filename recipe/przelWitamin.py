def PrzeliczanieWit(dodanySkladnik,to_updade,rodzaj,ilosc):
    if dodanySkladnik=='Witamina A':#to_update {'skladnik': 'Witamina A', 'jednostka_z_recepty': 'solutio', 'ilosc_na_recepcie': '3', 'producent': 'Hasco 4500j.m./ml', 'gestosc': '1.082'}
        if to_updade['jednostka_z_recepty']=='gramy_roztworu':#'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            to_updade['opakowania']=str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])*10),3))
            if to_updade['producent']=='Hasco 45000j.m./ml':
                to_updade['jednostki']=str(round(((float(to_updade['ilosc_na_recepcie'])/float(to_updade['gestosc']))*45000),3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc']))*28, 3))
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])), 3))
                to_updade['gramy']=to_updade['ilosc_na_recepcie']
                to_updade['gramy_roztworu'] = to_updade['ilosc_na_recepcie']
            elif to_updade['producent']=='Medana 50000j.m./ml':
                to_updade['jednostki']=str(round((float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc']))*50000),3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])) * 30, 3))
                to_updade['mililitry']= str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])),3))
                to_updade['gramy'] = to_updade['ilosc_na_recepcie']
                to_updade['gramy_roztworu'] = to_updade['ilosc_na_recepcie']
        elif to_updade['jednostka_z_recepty'] == 'jednostki':  # 'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            if to_updade['producent'] == 'Hasco 45000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 45000, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 45000)*float(to_updade['gestosc']), 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 45000)*float(to_updade['gestosc']), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 45000 * 28, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 450000, 3))
                to_updade['jednostki'] = to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) , 3))
            elif to_updade['producent'] == 'Medana 50000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 50000, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 50000*float(to_updade['gestosc'])), 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 50000*float(to_updade['gestosc'])), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 50000 * 30, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 500000, 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) , 3))
        elif to_updade['jednostka_z_recepty'] == 'krople':  # 'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            if to_updade['producent'] == 'Hasco 45000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28)*float(to_updade['gestosc']), 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28 * 45000, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 280, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28)*float(to_updade['gestosc']), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) , 3))
            elif to_updade['producent'] == 'Medana 50000j.m./ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28) * float(to_updade['gestosc']), 3))
                to_updade['jednostki'] = str(round(float(to_updade['ilosc_na_recepcie']) / 28 * 50000, 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 280, 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 28) * float(to_updade['gestosc']), 3))
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']), 3))
    elif dodanySkladnik == 'Oleum Menthae piperitae':
        if to_updade['jednostka_z_recepty']=='gramy':#'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) * 51, 0))
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])), 3))
                to_updade['gramy'] = to_updade['ilosc_na_recepcie']
        elif to_updade['jednostka_z_recepty']=='krople':#'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
                to_updade['gramy'] = str(round(float(to_updade['ilosc_na_recepcie']) * 0.020, 3))
                to_updade['mililitry'] = str(round((float(to_updade['ilosc_na_recepcie'])*0.020) / (float(to_updade['gestosc'])), 3))
                to_updade['krople'] = to_updade['ilosc_na_recepcie']
    elif dodanySkladnik=='Witamina E':#to_update {'skladnik': 'Witamina A', 'jednostka_z_recepty': 'solutio', 'ilosc_na_recepcie': '3', 'producent': 'Hasco 4500j.m./ml', 'gestosc': '1.082'}
        if to_updade['jednostka_z_recepty']=='gramy_roztworu':#'jednostka_z_recepty','solutio','opakowania','gramy','jednostki'
            to_updade['opakowania']=str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])*10),3))
            to_updade['gramy_czystej_vit_e'] = str(round((float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc']))) * 0.3, 3))
            to_updade['gramy'] = str(round(float(to_updade['ilosc_na_recepcie']), 3))
            to_updade['gramy_roztworu'] = str(round(float(to_updade['ilosc_na_recepcie']), 3))
            if to_updade['producent']=='Hasco 0,3g/ml':
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc']))*30, 0))
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])), 3))
            elif to_updade['producent']=='Medana 0,3g/ml':
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['gestosc'])) * 27, 0))
                to_updade['mililitry']= str(round(float(to_updade['ilosc_na_recepcie'])/(float(to_updade['gestosc'])),3))
        elif to_updade['jednostka_z_recepty'] == 'gramy_czystej_vit_e':
            to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 0.3, 3))
            to_updade['gramy_czystej_vit_e'] = str(round(float(to_updade['ilosc_na_recepcie']), 3))
            to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 3.0, 3))
            to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 0.3) * float(to_updade['gestosc']), 3))
            to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 0.3) * float(to_updade['gestosc']), 3))
            if to_updade['producent'] == 'Hasco 0,3g/ml':
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 0.3 * 30, 3))
            elif to_updade['producent'] == 'Medana 0,3g/ml':
                to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']) / 0.3 * 27, 3))
        elif to_updade['jednostka_z_recepty'] == 'krople':
            to_updade['krople'] = str(round(float(to_updade['ilosc_na_recepcie']), 3))
            if to_updade['producent'] == 'Hasco 0,3g/ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 30, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 30)*float(to_updade['gestosc']), 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 30) * float(to_updade['gestosc']), 3))
                to_updade['gramy_czystej_vit_e'] = str(round((float(to_updade['ilosc_na_recepcie']) / 30) * float(to_updade['gestosc']), 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 300, 3))
                to_updade['gramy_czystej_vit_e'] = str(round(float(to_updade['ilosc_na_recepcie']) / 90, 3))
            elif to_updade['producent'] == 'Medana 0,3g/ml':
                to_updade['mililitry'] = str(round(float(to_updade['ilosc_na_recepcie']) / 27, 3))
                to_updade['gramy_roztworu'] = str(round((float(to_updade['ilosc_na_recepcie']) / 27) * float(to_updade['gestosc']), 3))
                to_updade['gramy'] = str(round((float(to_updade['ilosc_na_recepcie']) / 27) * float(to_updade['gestosc']), 3))
                to_updade['gramy_czystej_vit_e'] = str(round((float(to_updade['ilosc_na_recepcie']) / 27) * float(to_updade['gestosc']), 3))
                to_updade['opakowania'] = str(round(float(to_updade['ilosc_na_recepcie']) / 270, 3))
                to_updade['gramy_czystej_vit_e'] = str(round(float(to_updade['ilosc_na_recepcie']) / 81, 3))
    if dodanySkladnik == 'Nystatyna':
        if to_updade['jednostka_z_recepty'] == 'jednostki':
            to_updade['gramy']=str(round(float(to_updade['ilosc_na_recepcie']) / (float(to_updade['UI_w_mg'])*1000), 3))
    if rodzaj == 'czopki_i_globulki':
        if 'krople' in to_updade:
            to_updade['krople']=str(round(float(to_updade['krople'])*float(ilosc),3))
        if 'mililitry' in to_updade:
            to_updade['mililitry'] = str(round(float(to_updade['mililitry']) * float(ilosc), 3))
        if 'opakowania' in to_updade:
            to_updade['opakowania'] = str(round(float(to_updade['opakowania']) * float(ilosc), 3))
        if 'jednostki' in to_updade:
            to_updade['jednostki'] = str(round(float(to_updade['jednostki']) * float(ilosc), 3))
        if 'gramy' in to_updade:
            to_updade['gramy'] = str(round(float(to_updade['gramy']) * float(ilosc), 3))
        if 'gramy_roztworu' in to_updade:
            to_updade['gramy_roztworu'] = str(round(float(to_updade['gramy_roztworu']) * float(ilosc), 3))
    return to_updade
