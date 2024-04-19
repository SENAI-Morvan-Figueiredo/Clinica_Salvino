from django.contrib import admin

from .models import Convenio, Tratamento, Consulta

# Register your models here.
admin.site.register(Convenio)
admin.site.register(Tratamento)
admin.site.register(Consulta)

