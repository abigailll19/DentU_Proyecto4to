from rest_framework import serializers
from decimal import Decimal
from .servicio_serializer import ServicioSerializer
from servicios.models.mediotransporte import MedioTransporte


class MedioTransporteSerializer(ServicioSerializer):
    class Meta(ServicioSerializer.Meta):
        model = MedioTransporte
        fields = ServicioSerializer.Meta.fields + [
            'id_transporte',
            'nombreEmpresa',
            'tipo_transporte',
            'nombreCooperativa',
            'ruta',
            'tarifa',
            'distancia_km',
            'tiempo_estimado_min'
        ]
        read_only_fields = ['id_transporte']
    
    def validate_nombreEmpresa(self, value):
        """Validar el nombre de la empresa"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre de la empresa no puede estar vacío")
        if len(value) < 3:
            raise serializers.ValidationError("El nombre de la empresa debe tener al menos 3 caracteres")
        if len(value) > 150:
            raise serializers.ValidationError("El nombre de la empresa no puede exceder 150 caracteres")
        return value.strip()
    
    def validate_tipo_transporte(self, value):
        """Validar el tipo de transporte"""
        tipos_validos = ['bus', 'taxi', 'metro', 'a_pie', 'bicicleta', 'otro']
        if value.lower() not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de transporte inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value.lower()
    
    def validate_nombreCooperativa(self, value):
        """Validar el nombre de la cooperativa"""
        if value and len(value.strip()) > 200:
            raise serializers.ValidationError("El nombre de la cooperativa no puede exceder 200 caracteres")
        return value.strip() if value else None
    
    def validate_tarifa(self, value):
        """Validar la tarifa"""
        if value is not None:
            if value < Decimal('0'):
                raise serializers.ValidationError("La tarifa no puede ser negativa")
            if value > Decimal('999.99'):
                raise serializers.ValidationError("La tarifa no puede exceder 999.99")
        return value
    
    def validate_distancia_km(self, value):
        """Validar la distancia en kilómetros"""
        if value is not None:
            if value < 0:
                raise serializers.ValidationError("La distancia no puede ser negativa")
            if value > 1000:
                raise serializers.ValidationError("La distancia no puede exceder 1000 km")
        return value
    
    def validate_tiempo_estimado_min(self, value):
        """Validar el tiempo estimado en minutos"""
        if value is not None:
            if value < 1:
                raise serializers.ValidationError("El tiempo estimado debe ser al menos 1 minuto")
            if value > 1440:  # 24 horas en minutos
                raise serializers.ValidationError("El tiempo estimado no puede exceder 24 horas")
        return value
