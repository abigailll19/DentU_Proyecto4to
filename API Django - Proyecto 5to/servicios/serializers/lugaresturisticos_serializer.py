from rest_framework import serializers
from .servicio_serializer import ServicioSerializer
from servicios.models.lugaresTuristicos import LugaresTuristico


class LugaresTuristicoSerializer(ServicioSerializer):
    class Meta(ServicioSerializer.Meta):
        model = LugaresTuristico
        fields = ServicioSerializer.Meta.fields + ['nombre_lugar', 'ubicacion', 'fotos']
        read_only_fields = ['fotos']
    
    def validate_nombre_lugar(self, value):
        """Validar el nombre del lugar turístico"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre del lugar no puede estar vacío")
        if len(value) < 3:
            raise serializers.ValidationError("El nombre del lugar debe tener al menos 3 caracteres")
        if len(value) > 255:
            raise serializers.ValidationError("El nombre del lugar no puede exceder 255 caracteres")
        return value.strip()
    
    def validate_ubicacion(self, value):
        """Validar la ubicación"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("La ubicación no puede estar vacía")
        if len(value) < 5:
            raise serializers.ValidationError("La ubicación debe tener al menos 5 caracteres")
        if len(value) > 255:
            raise serializers.ValidationError("La ubicación no puede exceder 255 caracteres")
        return value.strip()