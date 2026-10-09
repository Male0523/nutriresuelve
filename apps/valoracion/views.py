from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.pacientes.models import Paciente
from apps.recomendaciones.models import Alimento, Recomendacion
from .models import Consulta
from .inferencia import evaluar_reglas, calcular_imc
from .groq_ia import generar_plan_alimentario
from django.contrib.auth.decorators import login_required


@login_required
def valorar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        peso = request.POST.get('peso_kg')
        talla = request.POST.get('talla_cm')

        imc = calcular_imc(peso, talla)
        regla = evaluar_reglas(
            imc=imc,
            edad=paciente.edad,
            nivel_se=paciente.nivel_socioeconomico,
            nivel_actividad=paciente.nivel_actividad
        )

        if not regla:
            messages.error(request, 'No se encontró una regla para este paciente. Contacta al administrador.')
            return redirect('valorar_paciente', paciente_id=paciente.id)

        consulta = Consulta.objects.create(
            paciente=paciente,
            peso_kg=peso,
            talla_cm=talla,
            imc_calculado=imc,
            clasificacion=regla.clasificacion,
            regla_activada=regla,
            observaciones=regla.observacion
        )

        # Alimentos PAE filtrando alergias
        alergias = paciente.alergias.values_list('descripcion', flat=True)
        alimentos = Alimento.objects.filter(disponible_pae=True).exclude(nombre__in=alergias)

        # Generar plan con Gemini
        plan_ia = generar_plan_alimentario(paciente, regla.clasificacion, alimentos)
        print("GEMINI RESULTADO:", plan_ia)

        recomendacion = Recomendacion.objects.create(
            consulta=consulta,
            grupos_alimentarios=regla.clasificacion,
            detalle=regla.observacion,
            detalle_ia=plan_ia
        )
        recomendacion.alimentos.set(alimentos)

        messages.success(request, f'Valoración completada — {regla.clasificacion}')
        return redirect('ver_recomendacion', recomendacion_id=recomendacion.id)

    return render(request, 'valoracion/valorar.html', {'paciente': paciente})

@login_required
def ver_recomendacion(request, recomendacion_id):
    recomendacion = get_object_or_404(Recomendacion, id=recomendacion_id)
    return render(request, 'valoracion/recomendacion.html', {'recomendacion': recomendacion})