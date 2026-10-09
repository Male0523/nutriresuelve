from django.db import models


class EPS(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = "EPS"
        verbose_name_plural = "EPS"

    def __str__(self):
        return self.nombre


class RepresentanteLegal(models.Model):
    nombre_completo = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    parentesco = models.CharField(max_length=50, choices=[
        ('padre', 'Padre'),
        ('madre', 'Madre'),
        ('abuelo', 'Abuelo/a'),
        ('tio', 'Tío/a'),
        ('otro', 'Otro'),
    ])

    class Meta:
        verbose_name = "Representante legal"

    def __str__(self):
        return self.nombre_completo


class Paciente(models.Model):
    NIVEL_SE = [('bajo', 'Bajo'), ('medio', 'Medio'), ('alto', 'Alto')]
    NIVEL_ACTIVIDAD = [('baja', 'Baja'), ('moderada', 'Moderada'), ('alta', 'Alta')]

    nombre_completo = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2)
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2)
    eps = models.ForeignKey(EPS, on_delete=models.SET_NULL, null=True, blank=True)
    representante = models.ForeignKey(RepresentanteLegal, on_delete=models.SET_NULL, null=True, blank=True)
    nivel_socioeconomico = models.CharField(max_length=20, choices=NIVEL_SE, default='bajo')
    nivel_actividad = models.CharField(max_length=20, choices=NIVEL_ACTIVIDAD, default='baja')
    institucion = models.CharField(max_length=200, blank=True, help_text="Colegio o fundación")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Paciente"
        ordering = ['-fecha_registro']

    @property
    def edad(self):
        from datetime import date
        hoy = date.today()
        years = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            years -= 1
        return years

    @property
    def imc(self):
        talla_m = float(self.talla_cm) / 100
        return round(float(self.peso_kg) / (talla_m ** 2), 2)

    def __str__(self):
        return self.nombre_completo


class Alergia(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='alergias')
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.paciente} — {self.descripcion}"


class RestriccionMedica(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='restricciones')
    descripcion = models.CharField(max_length=200)
    medico_tratante = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.paciente} — {self.descripcion}"