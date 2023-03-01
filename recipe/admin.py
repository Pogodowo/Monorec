from django.contrib import admin



from .models import Receptura,Skladnik,Licznik_receptur
admin.site.register(Receptura)
admin.site.register(Skladnik)
admin.site.register(Licznik_receptur)

