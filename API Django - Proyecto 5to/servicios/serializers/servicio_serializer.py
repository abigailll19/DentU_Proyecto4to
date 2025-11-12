from rest_framework import serializers
from decimal import Decimal
from servicios.models.servicio import Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['descripcion', 'tipo_servicio', 'horario', 'precio', 'medioTransporte']
        
    def validate_descripcion(self, value):
        """Validar la descripción del servicio"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("La descripción no puede estar vacía")
        if len(value) < 10:
            raise serializers.ValidationError("La descripción debe tener al menos 10 caracteres")
        if len(value) > 200:
            raise serializers.ValidationError("La descripción no puede exceder 200 caracteres")
        return value.strip()
    
    def validate_tipo_servicio(self, value):
        """Validar el tipo de servicio"""
        tipos_validos = [
            'transporte', 
            'hospedaje', 
            'alimentacion', 
            'turismo', 
            'entretenimiento'
        ]
        if value.lower() not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de servicio inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value.lower()
    
    def validate_horario(self, value):
        """Validar el formato del horario"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El horario no puede estar vacío")
        if len(value) > 100:
            raise serializers.ValidationError("El horario no puede exceder 100 caracteres")
        return value.strip()
    
    def validate_precio(self, value):
        """Validar el precio"""
        if value <= Decimal('0'):
            raise serializers.ValidationError("El precio debe ser mayor que 0")
        if value > Decimal('9999.99'):
            raise serializers.ValidationError("El precio no puede exceder 9999.99")
        return value