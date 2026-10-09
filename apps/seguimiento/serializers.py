from rest_framework import serializers # type: ignore
from .models import Seguimiento

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = '__all__'