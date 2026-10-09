from django.db import models
from apps.valoracion.models import Consulta


class CategoriaAlimento(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categoría de alimento"
        verbose_name_plural = "Categorías de alimentos"

    def __str__(self):
        return self.nombre


class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaAlimento, on_delete=models.CASCADE, related_name='alimentos')
    disponible_pae = models.BooleanField(default=True)
    alergeno = models.BooleanField(default=False, help_text="¿Es un alérgeno común?")
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = "Alimento"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre


class Recomendacion(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='recomendacion')
    alimentos = models.ManyToManyField(Alimento, blank=True)
    grupos_alimentarios = models.TextField()
    detalle = models.TextField()
    detalle_ia = models.TextField(blank=True, help_text="Texto generado por Gemini")
    fecha_generacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recomendación"

    def __str__(self):
        return f"Recomendación — {self.consulta}"