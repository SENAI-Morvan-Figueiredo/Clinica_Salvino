from django.contrib import admin
from .models import Paciente, Prontuario,Documentos, Consulta, CadCartao, CadConvenio, Pagamento


# Register your models here.
admin.site.register(Paciente)
admin.site.register(Prontuario)
admin.site.register(Documentos)
admin.site.register(Consulta)
admin.site.register(CadConvenio)
admin.site.register(CadCartao)
admin.site.register(Pagamento)
