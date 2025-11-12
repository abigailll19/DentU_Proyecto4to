from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuarios.models import Turista

class TuristaSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    preferencias = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True,
        help_text='Lista de preferencias del turista'
    )
    
    class Meta:
        model = Turista
        fields = ['id', 'nombre', 'correo', 'contrasena', 'tipo', 
                  'idiomaPreferido', 'preferencias']
        read_only_fields = ['id']
    
    def validate_preferencias(self, value):
        """Validar preferencias"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Las preferencias deben ser una lista")
        
        # Limitar número de preferencias
        if len(value) > 20:
            raise serializers.ValidationError("Máximo 20 preferencias permitidas")
        
        # Validar cada preferencia
        preferencias_validas = []
        for pref in value:
            if not isinstance(pref, str):
                raise serializers.ValidationError("Cada preferencia debe ser texto")
            pref_clean = pref.strip().lower()
            if pref_clean and pref_clean not in preferencias_validas:
                preferencias_validas.append(pref_clean)
        
        return preferencias_validas
    
    def validate(self, attrs):
        """Validación a nivel de objeto"""
        attrs['tipo'] = 'turista'
        return attrs
    
    def create(self, validated_data):
        """Hashear contraseña"""
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)
