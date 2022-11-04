from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home,name='home'),
    # path('mojerec',views.mojeRec,name='mojerec'),
    path('dodajrec',views.dodajRec,name='dodajrec'),
    path('receptura/(<int:receptura_id>)',views.receptura,name='receptura'),
    # path('formJson/<str:skl>/', views.formJson, name='formJson'),
    path('receptura/formJson/<str:skl>/', views.formJson, name='formJson'),
    # #`receptura/dodajskl/${ sklId }/`
    path('receptura/dodajskl/<str:sklId>/', views.dodajsklJson, name='dodajsklJson'),
    # #path('receptura/dodajskl', views.dodajsklJson, name='dodajsklJson'),`aktualizujTabela/${sklId}/`
    path('receptura/aktualizujTabela/<str:sklId>/', views.aktualizujTabela, name='aktualizujTabela'),
    # path('spisSkl/<str:sklId>/', views.aktualizujTabela, name='spisSkl'),
    path('receptura/delSkl/<int:id>/', views.delSkl, name='delSkl'),
    path('receptura/editFormJson/<str:skl>/', views.editFormJson, name='editformJson'),
    path('receptura/edytujskl/<str:pk>/', views.edytujsklJson, name='edytujsklJson'),
    # path('receptura/slownik/', views.slownikJson, name='slownikJson'),
    path('dodajRecForm/', views.dodajRecForm, name='dodajRecForm'),
    path('receptura/dodajRecForm/', views.dodajRecForm, name='dodajRecForm'),
    path('dodawanieRecJson/', views.dodawanieRecJson, name='dodawanieRecJson'),
    path('receptura/dodawanieRecJson/', views.dodawanieRecJson, name='dodawanieRecJson'),
    # path('usunRec/<str:id>/', views.usunRec, name='usunRec'),
    # path('receptura/paramRec/<str:recId>/', views.ParamRecJson, name='ParamRecJson'),
    path('receptura/obliczeniaOlCac/<str:sklId>/', views.obliczeniaOlCac, name='obliczeniaOlCac'),
    path('receptura/obliczeniaEt/<str:sklId>/', views.obliczeniaEt, name='obliczeniaEt'),
    path('aktualnaRec', views.aktualnaRec, name='aktualnaRec'),







]
