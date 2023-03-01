from django.db import models
from datetime import datetime,timedelta
from django.utils import timezone


from django.contrib.sessions.models import Session
def get_time():
    return datetime.now()+timedelta(hours=1)

class RecepturaManager(models.Manager):
    def select_old(self):
        seven_days_ago = timezone.now() - timedelta(days=7)
        return self.filter(date__lt=seven_days_ago)

class Receptura(models.Model):
    nazwa = models.CharField(max_length=20)
    date = models.DateTimeField(default = get_time)
    rodzaj = models.TextField( blank=True, null=True)
    czopki_czy_globulki = models.TextField( blank=True, null=True)
    ilosc_czop_glob = models.CharField(max_length=40, blank=True, null=True, default='')
    masa_docelowa_czop_glob = models.CharField(max_length=40, blank=True, null=True, default='')
    czy_ilosc_oleum_pomnozyc = models.TextField( blank=True, null=True)
    ilosc_masci = models.CharField(max_length=40, blank=True, null=True, default='')
    ilosc_gramow = models.CharField(max_length=40, blank=True, null=True, default='')
    session = models.ForeignKey(Session, null=True, on_delete=models.CASCADE)
    objects = RecepturaManager()

    def __str__(self):
        return self.rodzaj +'       '+ str(self.date)[:21]


class Skladnik(models.Model):
    receptura_id = models.ForeignKey(Receptura, on_delete=models.CASCADE)
    producenci = (('1', 'Hasco 4500j.m./ml'), ('2', 'Medana 50000j.m./ml'), ('3', 'Hasco 0,3g/ml'))
    skladnik = models.CharField(max_length=40)
    jednostka_z_recepty = models.CharField(max_length=40, blank=True, default='gramy')
    ilosc_na_recepcie = models.CharField(max_length=40, blank=True, null=True, default='0')
    gramy = models.CharField(max_length=40, default='0')
    mililitry = models.CharField(max_length=40, default='0')
    solutio = models.CharField(max_length=40, default='0')
    krople = models.CharField(max_length=40, default='0')
    opakowania = models.CharField(max_length=40, default='0')
    jednostki = models.CharField(max_length=40, default='0')
    gestosc = models.CharField(max_length=40, default='0')
    sztuki = models.CharField(max_length=40, default='0')
    tabletki = models.CharField(max_length=40, default='0')
    czesci = models.CharField(max_length=40, default='0')
    producent = models.CharField(max_length=40, default='0')
    aa = models.CharField(max_length=20, default='off')
    obey = models.IntegerField(null=True, default=0)
    sumg = models.IntegerField(default=0)
    aa_ad = models.CharField(max_length=20, default='off')
    aa_ad_gramy = models.CharField(max_length=40, default='0')
    show = models.BooleanField(default=True)
    dodaj_wode = models.CharField(max_length=20, default='off')
    pozadane_stezenie = models.CharField(max_length=40, blank=True, null=True, default='')
    uzyte_stezenie = models.CharField(max_length=40, blank=True, null=True, default='')
    ilosc_etanolu = models.CharField(max_length=40, blank=True, null=True, default='')
    ilosc_wody_do_etanolu = models.CharField(max_length=40, blank=True, null=True, default='0')
    qs = models.CharField(max_length=20, default='off')
    ad = models.CharField(max_length=20, default='off')
    woda_mocznik = models.CharField(max_length=40, default='0')
    UI_w_mg = models.CharField(max_length=40, default='6756')
    czy_zlozyc_roztwor_ze_skladnikow_prostych = models.CharField(max_length=20, default='off')
    woda_kwas_borowy = models.CharField(max_length=40, default='0')
    ilosc_kwasu_borowego_do_roztworu = models.CharField(max_length=40, default='0')
    calkowita_ilosc_gramow_wody = models.CharField(max_length=40, default='0')
    czy_powiekszyc_mase_oleum = models.CharField(max_length=20, default='off')
    gramy_czystej_vit_e = models.CharField(max_length=20, default='0')
    gramy_roztworu = models.CharField(max_length=20, default='0')

    def __str__(self):
        return self.skladnik

    # class Stats (models.Model):
    #     ilosc_receptur = models.IntegerField(default=0)
    #     def __str__(self):
    #         return self.ilosc_receptur




class Licznik_receptur(models.Model):
    ilosc_receptur=models.IntegerField(default=0)
    def __str__(self):
        return str(self.ilosc_receptur)
