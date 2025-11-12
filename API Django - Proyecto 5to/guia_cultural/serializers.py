from rest_framework import serializers
from .models import GuiaCultural

class GuiaCulturalSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuiaCultural
        fields = ['id', 'titulo', 'descripcion', 'categoria', 'contenido']
        read_only_fields = ['id']

    def validate_titulo(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('El título no puede estar vacío')
        if len(value) > 200:
            raise serializers.ValidationError('El título no puede exceder 200 caracteres')
        return value.strip()

    def validate_categoria(self, value):
        categorias_validas = [
            'normas_culturales', 'frases_basicas', 'costumbres', 'etiqueta', 'historia', 'gastronomia', 'arte', 'otro'
        ]
        if value.lower() not in categorias_validas:
            raise serializers.ValidationError(
                f'Categoría inválida. Opciones: {", ".join(categorias_validas)}'
            )
        return value.lower()

    def validate_descripcion(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('La descripción no puede estar vacía')
        if len(value) < 10:
            raise serializers.ValidationError('La descripción debe tener al menos 10 caracteres')
        return value.strip()

    def validate_contenido(self, value):
        if value and len(value) > 5000:
            raise serializers.ValidationError('El contenido no puede exceder 5000 caracteres')
        return value.strip() if value else value
