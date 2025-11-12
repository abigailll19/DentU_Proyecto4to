from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuarios.models.propietario import Propietario


class PropietarioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Propietario"""
    contrasena = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        """Meta del serializer Propietario"""
        model = Propietario
        fields = ['id', 'nombre', 'correo', 'contrasena', 'tipo', 
                  'idiomaPreferido', 'tipo_negocio']
        read_only_fields = ['id']
    
    def validate_tipo_negocio(self, value):
        """Validar tipo de negocio"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El tipo de negocio es obligatorio")
        
        tipos_validos = ['hotel', 'restaurante', 'transporte', 'tour', 'otro']
        if value.lower() not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de negocio inválido. Opciones: {', '.join(tipos_validos)}"
            )
        return value.lower()
    
    def validate(self, attrs):
        """Validación a nivel de objeto"""
        # Asegurar que el tipo sea 'propietario'
        attrs['tipo'] = 'propietario'
        return attrs
    
    def create(self, validated_data):
        """Hashear contraseña"""
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)

