from rest_framework import serializers
from servicios.models.atraccion import Atraccion
from .servicio_serializer import ServicioSerializer



class AtraccionSerializer(ServicioSerializer):
    class Meta(ServicioSerializer.Meta):
        model = Atraccion
        fields = ServicioSerializer.Meta.fields + ['nombre_lugar']
    
    def validate_nombre_lugar(self, value):
        """Validar el nombre de la atracción"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre de la atracción no puede estar vacío")
        if len(value) < 3:
            raise serializers.ValidationError("El nombre de la atracción debe tener al menos 3 caracteres")
        if len(value) > 200:
            raise serializers.ValidationError("El nombre de la atracción no puede exceder 200 caracteres")
        return value.strip()