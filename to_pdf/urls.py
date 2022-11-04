from . import views
from django.urls import path

app_name = 'to_pdf'
urlpatterns=[
path('<str:pk>/',views.to_pdf,name='to_pdf'),
]