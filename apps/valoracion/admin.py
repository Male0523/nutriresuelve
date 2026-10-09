from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReglaExperto, Consulta

@admin.register(ReglaExperto)
class ReglaExpertoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'clasificacion', 'imc_min', 'imc_max', 'edad_min', 'edad_max', 'nivel_se', 'prioridad']
    ordering = ['-prioridad']

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'imc_calculado', 'clasificacion', 'validado_por_nutricionista']
    list_filter = ['validado_por_nutricionista', 'clasificacion']
    search_fields = ['paciente__nombre_completo']