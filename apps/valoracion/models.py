from django.db import models
from apps.pacientes.models import Paciente


class ReglaExperto(models.Model):
    NIVELES_SE = [('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto'), ('cualquiera', 'Cualquiera')]
    NIVELES_ACTIVIDAD = [('baja', 'Baja'), ('moderada', 'Moderada'), ('alta', 'Alta'), ('cualquiera', 'Cualquiera')]

    codigo = models.CharField(max_length=20, unique=True)  # R-001, R-002...
    descripcion = models.CharField(max_length=200)
    imc_min = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    imc_max = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    edad_min = models.IntegerField(null=True, blank=True)
    edad_max = models.IntegerField(null=True, blank=True)
    nivel_se = models.CharField(max_length=20, choices=NIVELES_SE, default='cualquiera')
    nivel_actividad = models.CharField(max_length=20, choices=NIVELES_ACTIVIDAD, default='cualquiera')
    clasificacion = models.CharField(max_length=100)
    observacion = models.TextField()
    prioridad = models.IntegerField(default=0, help_text="Mayor número = se evalúa primero")

    class Meta:
        verbose_name = "Regla experto"
        verbose_name_plural = "Reglas experto"
        ordering = ['-prioridad']

    def __str__(self):
        return f"{self.codigo} — {self.clasificacion}"


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2)
    imc_calculado = models.DecimalField(max_digits=5, decimal_places=2)
    clasificacion = models.CharField(max_length=100)
    regla_activada = models.ForeignKey(ReglaExperto, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    validado_por_nutricionista = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Consulta"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.paciente} — {self.fecha.date()}"