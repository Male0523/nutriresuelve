from django.contrib import admin
from .models import CategoriaAlimento, Alimento, Recomendacion

@admin.register(CategoriaAlimento)
class CategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'disponible_pae', 'alergeno']
    list_filter = ['categoria', 'disponible_pae', 'alergeno']
    search_fields = ['nombre']

@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    list_display = ['consulta', 'fecha_generacion']