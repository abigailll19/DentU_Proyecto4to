from rest_framework import serializers
from .lugaresturisticos_serializer import LugaresTuristicoSerializer
from servicios.models.hotel import Hotel


class HotelSerializer(LugaresTuristicoSerializer):
    class Meta(LugaresTuristicoSerializer.Meta):
        model = Hotel
        fields = LugaresTuristicoSerializer.Meta.fields + ['clasificacion', 'servicios_hotel']
    
    def validate_clasificacion(self, value):
        """Validar la clasificación del hotel"""
        clasificaciones_validas = ['1', '2', '3', '4', '5']
        if value not in clasificaciones_validas:
            raise serializers.ValidationError(
                f"Clasificación inválida. Debe ser una de: {', '.join(clasificaciones_validas)} estrellas"
            )
        return value
    
    def validate_servicios_hotel(self, value):
        """Validar los servicios del hotel"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Los servicios del hotel no pueden estar vacíos")
        if len(value) > 255:
            raise serializers.ValidationError("Los servicios del hotel no pueden exceder 255 caracteres")
        return value.strip()