from django.contrib import admin

from .models import Convenio, Tratamento, PlanoConvenio, BandeiraCartao, Pix

# Register your models here.
admin.site.register(Convenio)
admin.site.register(Tratamento)
admin.site.register(PlanoConvenio)
admin.site.register(BandeiraCartao)
admin.site.register(Pix)
