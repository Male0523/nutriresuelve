import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente, EPS, RepresentanteLegal, Alergia

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

@login_required
def registrar_paciente(request):
    if request.method == 'POST':
        # Detectar si la petición viene enviada como JSON (fetch de sincronización JS) o Formulario estándar
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        # Extraer campos garantizando valores por defecto sin nulos que rompan la base de datos
        rep_nombre = data.get('rep_nombre', '').strip()
        rep_telefono = data.get('rep_telefono', '').strip()
        rep_parentesco = data.get('rep_parentesco', 'otro')

        if not rep_nombre:
            rep_nombre = "Sin Nombre Registrado"

        rep = RepresentanteLegal.objects.create(
            nombre_completo=rep_nombre,
            telefono=rep_telefono,
            parentesco=rep_parentesco,
        )

        paciente = Paciente.objects.create(
            nombre_completo=data.get('nombre_completo', '').strip(),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            peso_kg=data.get('peso_kg') or None,
            talla_cm=data.get('talla_cm') or None,
            nivel_socioeconomico=data.get('nivel_socioeconomico', 'bajo'),
            nivel_actividad=data.get('nivel_actividad', 'baja'),
            institucion=data.get('institucion', ''),
            representante=rep,
        )

        alergias = data.get('alergias', '')
        if alergias:
            for a in alergias.split(','):
                if a.strip():
                    Alergia.objects.create(paciente=paciente, descripcion=a.strip())

        return redirect('lista_pacientes')

    eps_list = EPS.objects.all()
    return render(request, 'pacientes/registro.html', {'eps_list': eps_list})

@login_required
def detalle_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    return render(request, 'pacientes/detalle.html', {'paciente': paciente})