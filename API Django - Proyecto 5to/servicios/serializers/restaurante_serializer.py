from rest_framework import serializers
from .lugaresturisticos_serializer import LugaresTuristicoSerializer
from servicios.models.restaurante import Restaurante


class RestauranteSerializer(LugaresTuristicoSerializer):
    class Meta(LugaresTuristicoSerializer.Meta):
        model = Restaurante
        fields = LugaresTuristicoSerializer.Meta.fields + ['tipoComida', 'propietario']
    
    def validate_tipoComida(self, value):
        """Validar el tipo de comida"""
        tipos_validos = [
            'italiana', 
            'mexicana', 
            'china', 
            'japonesa', 
            'ecuatoriana',
            'internacional',
            'mariscos',
            'vegetariana',
            'vegana',
            'rapida',
            'cafeteria',
            'otro'
        ]
        if value.lower() not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de comida inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value.lower()