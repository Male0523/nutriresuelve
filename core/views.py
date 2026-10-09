from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.pacientes.models import Paciente
from apps.valoracion.models import Consulta
from apps.recomendaciones.models import Recomendacion


@login_required
def dashboard(request):
    total_pacientes = Paciente.objects.count()
    total_consultas = Consulta.objects.count()
    total_recomendaciones = Recomendacion.objects.count()
    ultimos_pacientes = Paciente.objects.order_by('-fecha_registro')[:5]

    severos = Paciente.objects.filter(peso_kg__isnull=False)
    desnutricion_severa = sum(1 for p in severos if p.imc < 16)
    desnutricion_moderada = sum(1 for p in severos if 16 <= p.imc < 18.5)
    normal = sum(1 for p in severos if 18.5 <= p.imc <= 24.9)
    sobrepeso = sum(1 for p in severos if p.imc > 24.9)

    institucion_top = Paciente.objects.values('institucion').annotate(
        total=Count('id')
    ).order_by('-total').first()

    context = {
        'total_pacientes': total_pacientes,
        'total_consultas': total_consultas,
        'total_recomendaciones': total_recomendaciones,
        'ultimos_pacientes': ultimos_pacientes,
        'desnutricion_severa': desnutricion_severa,
        'desnutricion_moderada': desnutricion_moderada,
        'normal': normal,
        'sobrepeso': sobrepeso,
        'institucion_top': institucion_top,
    }
    return render(request, 'dashboard.html', context)


def error_404(request, exception):
    return render(request, '404.html', status=404)