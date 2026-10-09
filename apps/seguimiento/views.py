from django.shortcuts import render, get_object_or_404
from apps.pacientes.models import Paciente
from .models import Seguimiento
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def seguimiento_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    seguimientos = Seguimiento.objects.filter(paciente=paciente).order_by('fecha')
    consultas = paciente.consultas.order_by('fecha')

    # Datos para la gráfica
    fechas = [str(c.fecha.date()) for c in consultas]
    imcs = [float(c.imc_calculado) for c in consultas]

    context = {
        'paciente': paciente,
        'seguimientos': seguimientos,
        'consultas': consultas,
        'fechas': fechas,
        'imcs': imcs,
    }
    return render(request, 'seguimiento/seguimiento.html', context)

@login_required
def lista_seguimientos(request):
    from apps.pacientes.models import Paciente
    pacientes = Paciente.objects.annotate(
        total_consultas=Count('consultas')
    ).filter(total_consultas__gt=0).order_by('-total_consultas')
    return render(request, 'seguimiento/lista.html', {'pacientes': pacientes})