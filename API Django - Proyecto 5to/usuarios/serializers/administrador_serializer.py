from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuarios.models import Administrador
import re


class AdministradorSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(
        write_only=True,
        min_length=10,  # Más estricto para admin
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Administrador
        fields = ['id', 'nombre', 'correo', 'contrasena', 'tipo', 'idiomaPreferido']
        read_only_fields = ['id']
    
    def validate_contrasena(self, value):
        """Validación más estricta para administradores"""
        if len(value) < 10:
            raise serializers.ValidationError(
                "La contraseña de administrador debe tener al menos 10 caracteres"
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Debe contener al menos una mayúscula")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Debe contener al menos una minúscula")
        
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Debe contener al menos un número")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Debe contener al menos un carácter especial (!@#$%^&*...)"
            )
        
        return value
    
    def validate(self, attrs):
        """Validación a nivel de objeto"""
        attrs['tipo'] = 'administrador'
        return attrs
    
    def create(self, validated_data):
        """Hashear 
        """
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)