from .models import ReglaExperto


def evaluar_reglas(imc, edad, nivel_se, nivel_actividad):
    """
    Evalúa las reglas expertas en orden de prioridad.
    Retorna la regla que aplica o None si ninguna coincide.
    """
    reglas = ReglaExperto.objects.all()  # ya vienen ordenadas por prioridad

    for regla in reglas:
        if regla.imc_min is not None and imc < float(regla.imc_min):
            continue
        if regla.imc_max is not None and imc >= float(regla.imc_max):
            continue
        if regla.edad_min is not None and edad < regla.edad_min:
            continue
        if regla.edad_max is not None and edad > regla.edad_max:
            continue
        if regla.nivel_se != 'cualquiera' and regla.nivel_se != nivel_se:
            continue
        if regla.nivel_actividad != 'cualquiera' and regla.nivel_actividad != nivel_actividad:
            continue
        return regla  # primera regla que cumple todas las condiciones

    return None


def calcular_imc(peso_kg, talla_cm):
    talla_m = float(talla_cm) / 100
    return round(float(peso_kg) / (talla_m ** 2), 2)