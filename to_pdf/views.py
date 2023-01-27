from django.shortcuts import render
from recipe.models import Skladnik,Receptura
from .dane_do_wyswietlenia import dane_do_wyswietlenia as dane
import sys
import reportlab
import io
from django.http import FileResponse,response
from reportlab.pdfgen import canvas
#============================================================
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Indenter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter,A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm,cm
from django.conf import settings
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, Paragraph, PageBreak, Table, \
    TableStyle
from recipe.słownik_do_tabeli import table_dict
from recipe.wspolczynniki_wyparcia import wspolczynniki_wyparcia
from recipe.obliczenia import obliczeniaOlCacVisual,obliczeniaEtVisual

def to_pdf(request,pk):
    receptura = Receptura.objects.get(id=int(pk))

    Skladniki = Skladnik.objects.filter(receptura_id=int(pk)).order_by("pk")
    do_tabeli=[[''+ receptura.nazwa,receptura.date.strftime(" data utworzenia: %d-%m-%y godz: %H:%M") ],]
    rodzaj=''
    ilosc_czop_glob=''
    masa_czop_glob = ''
    if receptura.rodzaj!='czopki_i_globulki':
        rodzaj='rodzaj: '+ table_dict[receptura.rodzaj]
        #rodzaj = 'rodzaj: ' + słownik_do_tabeli['masc']
        do_tabeli2 = [[rodzaj]]
        brackets=[510]
    else:

        rodzaj='rodzaj: '+receptura.czopki_czy_globulki
        if receptura.czopki_czy_globulki=='czopki':
            ilosc_czop_glob='ilość czopków: '+receptura.ilosc_czop_glob
            masa_czop_glob='masa pojedynczego czopka: '+receptura.masa_docelowa_czop_glob+' g.'
        else:
            ilosc_czop_glob = 'ilość globulek: ' + receptura.ilosc_czop_glob
            masa_czop_glob = 'masa pojedynczej globulki: ' + receptura.masa_docelowa_czop_glob+' g.'
        do_tabeli2 = [[rodzaj, ilosc_czop_glob, masa_czop_glob]]
        brackets = [170, 170,170]

    #do_tabeli2 = [[rodzaj, ilosc_czop_glob,masa_czop_glob]]


    print('do_tabeli',do_tabeli)
    sys.stdout.flush()
    buffer = io.BytesIO()
    test=str(pk)
    p = canvas.Canvas(buffer, pagesize=A4)
    reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/to_pdf')
    pdfmetrics.registerFont(TTFont('polishFont', 'polishFont.ttf'))
    pdfmetrics.registerFont(TTFont('AbhayaLibre-Regular', 'AbhayaLibre-Regular.ttf'))
    p.setFont('AbhayaLibre-Regular', 32)
    x=250-len('Receptura '+receptura.nazwa[:24]+' ')*6
    p.drawString(x, 780, 'Receptura:'+receptura.nazwa[:24]+' ')

    # ======================================tabela==============================================
    name_bracket_size=90
    date_bracket_size=90
    # if len(receptura.nazwa[:24])*6>70:
    #     name_bracket_size=len(receptura.nazwa[:24])*4

    width = 500
    height = 500
    x = 30
    y=730
    #y = b - (a * 15)
    table = Table(do_tabeli, colWidths=[name_bracket_size * mm, date_bracket_size* mm,])

    ts = TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONT', (0, 0), (-1, -1), 'AbhayaLibre-Regular', 13),
                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP')])
    table.setStyle(ts)

    table.wrapOn(p, width, height)
    table.drawOn(p, x, y)
    x = 30
    y = 705
    # y = b - (a * 15)
    table1 = Table(do_tabeli2, colWidths=brackets)

    ts = TableStyle(
        [('GRID', (0, 0), (-1, -1), 0.5, colors.black), ('FONT', (0, 0), (-1, -1), 'AbhayaLibre-Regular', 13),
         ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'TOP')])
    table1.setStyle(ts)

    table1.wrapOn(p, width, height)
    table1.drawOn(p, x, y)
    #===========================recepta================================================================================
    x=30
    y=650
    p.setFont('polishFont', 13)
    p.drawString(x, y, 'Rp.')
    y=630
    def skladnik(skl):
        stri=''
        if skl.show==True:
            stri=stri+skl.skladnik+' '
            if skl.jednostka_z_recepty == 'gramy_roztworu':
                stri+=' sol. '
            if skl.jednostka_z_recepty == 'krople':
                stri+=' gtt. '
            if skl.skladnik == 'Etanol':
                stri+= skl.pozadane_stezenie+' °'
            if skl.aa=='on':
                stri=stri+' aa'
            elif skl.qs=='on':
                stri=stri+' qs'
            elif skl.ad=='on':
                stri=stri+' ad'
            elif skl.aa_ad=='on':
                stri=stri+' aa ad '

            if  skl.ilosc_na_recepcie!='' and float(skl.ilosc_na_recepcie)%1==0 :
                stri=stri+' '+format(float(skl.ilosc_na_recepcie), '.1f')
            elif  skl.ilosc_na_recepcie!='' and float(skl.ilosc_na_recepcie)%1!=0 :
                stri=stri+' '+ str(round(float(skl.ilosc_na_recepcie), 3))
            if skl.jednostka_z_recepty == 'jednostki':
                stri+=' j.m.'


        return stri
    for i in Skladniki:
        if i.show==True:
            p.drawString(x, y, skladnik(i))
            y=y-20
    if receptura.rodzaj == 'czopki_i_globulki':
        p.drawString(x, y, 'D.t.d. No '+receptura.ilosc_czop_glob )
    elif receptura.rodzaj == 'masc':
        p.drawString(x, y, 'M.f.Ung.' )
    elif receptura.rodzaj == 'receptura_plynna_zewnetrzna' or receptura.rodzaj == 'receptura_plynna_wewnetrzna' :
        p.drawString(x, y, 'M.f.Sol.' )
    x=300
    y=650
    count=1
    for i in Skladniki:

        p.setFont('AbhayaLibre-Regular', 13)
        p.drawString(x, y, str(count)+')  '+i.skladnik)
        p.line(x+250,y-5,x,y-5)
        count=count+1
        p.setFont('AbhayaLibre-Regular', 10)
        y=y-20
        p.drawString(x, y, 'dane z recepty:')
        if i.ilosc_na_recepcie!='':
            y=y-10
            p.setFont('AbhayaLibre-Regular', 11)
            p.drawString(x, y,  'jednostka na recepcie: '+i.jednostka_z_recepty+'   '+'ilość: '+ i.ilosc_na_recepcie)
        if i.producent!='0':
            y = y - 10
            p.drawString(x, y, 'producent: ' + i.producent + '   ' +'gęstość: ' + i.gestosc)
        y=y-10
        if receptura.rodzaj == 'czopki_i_globulki':
            p.drawString(x, y, 'wspóczynnik wyparcia: ' + str(wspolczynniki_wyparcia[i.skladnik]) )
            y = y - 1
        p.setLineWidth(0.25)
        p.line(x + 250, y - 2, x, y - 2)
        y=y-15
        p.drawString(x, y, 'obliczenia:')
        y=y-10
        a=0
        for j in range(len(dane[i.skladnik])):
            parametr=dane[i.skladnik][j]
            if parametr in table_dict:
                param_string=table_dict[parametr]+' : '+getattr(i, parametr )
                if len(param_string)<56:
                    p.drawString(x, y, param_string)
                else:
                    p.drawString(x, y, param_string[:50]+'-')
                    y=y-10
                    p.drawString(x, y, param_string[50:])
            else:
                param_string = parametr + ' : ' + getattr(i, parametr)
                if len(param_string) < 56:
                    p.drawString(x, y, param_string)
                else:
                    p.drawString(x, y, param_string[:50]+'-')
                    y = y - 10
                    p.drawString(x, y, param_string[50:])
            y=y-10



        p.setLineWidth(1)
        y=y-15
        if  y<80:
            p.showPage()
            y=800
    # if receptura.rodzaj == 'czopki_i_globulki' and jestOleum(pk):
    #      drawCzop(x, y, pk, p)

    if jestEtanol(pk):
        drawEtanol(x,y,pk,p)

    p.showPage()
    p.save()
    buffer.seek(0)


    return FileResponse(buffer, as_attachment=True, filename='receptura.pdf')



def drawEtanol(x,y,pk,p):
    y=y-50
    oblEt = obliczeniaEtVisual(pk)['obl']
    y = y - 10
    x = x - 270
    p.drawString(x, y, oblEt)
    oblEt1 = obliczeniaEtVisual(pk)['obl1']
    y = y - 15
    p.drawString(x, y, oblEt1)

    oblEt2 = obliczeniaEtVisual(pk)['obl2']
    y = y - 35
    p.drawString(x, y, oblEt2)

    licznik = obliczeniaEtVisual(pk)['licznik']
    y = y + 10
    x = x + 200
    p.drawString(x, y, licznik)
    p.line(x + 100, y - 7, x-40, y - 7)

    mianownik = obliczeniaEtVisual(pk)['mianownik']
    y = y - 20
    x=x+10
    p.drawString(x, y, mianownik)

    wynik = obliczeniaEtVisual(pk)['wynik']
    y = y + 10
    x = x + 100
    p.drawString(x, y, wynik)

    obl3 = obliczeniaEtVisual(pk)['obl3']
    y = y - 30
    x = x -310
    p.drawString(x, y, obl3)


def drawCzop(x,y,pk,p):
    oblOl = obliczeniaOlCacVisual(pk)['obliczenia']
    x = x - 200
    y = y - 10
    p.drawString(x, y, oblOl)

def jestEtanol(pk):

    Skladniki = Skladnik.objects.filter(receptura_id=int(pk)).order_by("pk")
    for i in Skladniki:
        if i.skladnik=='Etanol':
            return True
    return False


def jestOleum(pk):

    Skladniki = Skladnik.objects.filter(receptura_id=int(pk)).order_by("pk")
    for i in Skladniki:
        if i.skladnik=="Oleum Cacao":
            return True
    return False

