from rest_framework import serializers
from decimal import Decimal
from servicios.models.servicio import Servicio
from servicios.models.lugaresTuristicos import LugaresTuristico
from servicios.models.atraccion import Atraccion
from servicios.models.hotel import Hotel
from servicios.models.restaurante import Restaurante
from servicios.models.mediotransporte import MedioTransporte

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


class LugaresTuristicoSerializer(ServicioSerializer):
    class Meta(ServicioSerializer.Meta):
        model = LugaresTuristico
        fields = ServicioSerializer.Meta.fields + ['nombre_lugar', 'ubicacion']
    
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


class RestauranteSerializer(LugaresTuristicoSerializer):
    class Meta(LugaresTuristicoSerializer.Meta):
        model = Restaurante
        fields = LugaresTuristicoSerializer.Meta.fields + ['tipoComida']
    
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
