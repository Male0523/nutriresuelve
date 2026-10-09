from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EPS, RepresentanteLegal, Paciente, Alergia, RestriccionMedica

class AlergiaInline(admin.TabularInline):
    model = Alergia
    extra = 1

class RestriccionInline(admin.TabularInline):
    model = RestriccionMedica
    extra = 1

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'edad', 'imc', 'nivel_socioeconomico', 'institucion', 'fecha_registro']
    search_fields = ['nombre_completo', 'institucion']
    list_filter = ['nivel_socioeconomico', 'nivel_actividad']
    inlines = [AlergiaInline, RestriccionInline]

@admin.register(EPS)
class EPSAdmin(admin.ModelAdmin):
    pass

@admin.register(RepresentanteLegal)
class RepresentanteAdmin(admin.ModelAdmin):
    pass