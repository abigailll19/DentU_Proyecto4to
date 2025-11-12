import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from usuarios.models.usuario import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text='Mínimo 8 caracteres'
    )
    
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'correo', 'contrasena', 'tipo', 'idiomaPreferido']
        read_only_fields = ['id']
    
    def validate_nombre(self, value):
        """Validar que el nombre no esté vacío y tenga formato válido"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre no puede estar vacío")
        if len(value) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        if len(value) > 255:
            raise serializers.ValidationError("El nombre no puede exceder 255 caracteres")
        return value.strip()
    
    def validate_correo(self, value):
        """Validar formato de email y unicidad"""
        if not value:
            raise serializers.ValidationError("El correo es obligatorio")
        
        # Validar formato básico de email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Formato de correo inválido")
        
        return value.lower().strip()
    
    def validate_contrasena(self, value):
        """Validar contraseña segura"""
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una mayúscula")
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una minúscula")
        
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número")
        
        return value
    
    def validate_tipo(self, value):
        """Validar que el tipo sea válido"""
        tipos_validos = ['turista', 'propietario', 'administrador']
        if value.lower() not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de usuario inválido. Debe ser uno de: {', '.join(tipos_validos)}"
            )
        return value.lower()
    
    def validate_idioma_preferido(self, value):
        """Validar que el idioma sea soportado"""
        idiomas_soportados = ['es', 'en', 'fr', 'pt', 'de', 'it']
        if value.lower() not in idiomas_soportados:
            raise serializers.ValidationError(
                f"Idioma no soportado. Idiomas disponibles: {', '.join(idiomas_soportados)}"
            )
        return value.lower()
    
    def create(self, validated_data):
        """Hashear la contraseña al crear usuario"""
        validated_data['contrasena'] = make_password(validated_data['contrasena'])
        return super().create(validated_data)