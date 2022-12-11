from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home,name='home'),

    path('receptura/(<int:receptura_id>)',views.receptura,name='receptura'),
    path('receptura/formJson/<str:skl>/', views.formJson, name='formJson'),
    path('receptura/dodajskl/<str:sklId>/', views.dodajsklJson, name='dodajsklJson'),
    path('receptura/aktualizujTabela/<str:sklId>/', views.aktualizujTabela, name='aktualizujTabela'),
    path('receptura/delSkl/<int:id>/', views.delSkl, name='delSkl'),
    path('receptura/editFormJson/<str:skl>/', views.editFormJson, name='editformJson'),
    path('receptura/edytujskl/<str:pk>/', views.edytujsklJson, name='edytujsklJson'),
    path('dodajRecForm/', views.dodajRecForm, name='dodajRecForm'),
    path('receptura/dodajRecForm/', views.dodajRecForm, name='dodajRecForm'),
    path('dodawanieRecJson/', views.dodawanieRecJson, name='dodawanieRecJson'),
    path('receptura/dodawanieRecJson/', views.dodawanieRecJson, name='dodawanieRecJson'),
    path('receptura/obliczeniaOlCacJson/<str:sklId>/', views.obliczeniaOlCacJson, name='obliczeniaOlCac'),
    path('receptura/obliczeniaEtJson/<str:sklId>/', views.obliczeniaEtJson, name='obliczeniaEt'),
    path('aktualnaRec', views.aktualnaRec, name='aktualnaRec'),







]
