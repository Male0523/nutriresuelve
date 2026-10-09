from rest_framework import serializers # pyright: ignore[reportMissingImports]
from .models import Paciente

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'