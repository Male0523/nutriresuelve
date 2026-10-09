from django.contrib import admin
from .models import Seguimiento

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ['paciente', 'fecha', 'peso_kg', 'talla_cm', 'imc']
    search_fields = ['paciente__nombre_completo']
    list_filter = ['fecha']