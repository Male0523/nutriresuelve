from django.db import models
from apps.pacientes.models import Paciente


class Seguimiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='seguimientos')
    fecha = models.DateField()
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "Seguimiento"
        ordering = ['-fecha']

    @property
    def imc(self):
        talla_m = float(self.talla_cm) / 100
        return round(float(self.peso_kg) / (talla_m ** 2), 2)

    def __str__(self):
        return f"{self.paciente} — {self.fecha}"