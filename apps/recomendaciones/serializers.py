from rest_framework import serializers # type: ignore
from .models import Recomendacion

class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = '__all__'