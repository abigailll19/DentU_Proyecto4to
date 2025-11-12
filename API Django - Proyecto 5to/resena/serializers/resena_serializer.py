from rest_framework import serializers
from servicios.serializers import ServicioSerializer
from usuarios.serializers.usuario_serializer import UsuarioSerializer
from resena.models import Resena, FotoResena


class ResenaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Reseña.
    
    Permite la creación y validación de reseñas de usuarios sobre servicios turísticos.
    Incluye validaciones para todos los campos y maneja las relaciones con Usuario y Servicio.
    """
    
    # Campos anidados para mostrar detalles de las relaciones
    usuario_details = UsuarioSerializer(source='usuario', read_only=True)
    servicio_details = ServicioSerializer(source='servicio', read_only=True)
    
    class Meta:
        model = Resena
        fields = [
            'id',
            'autor',
            'destino',
            'mensaje',
            'calificacion',
            'fecha',
            'usuario',
            'usuario_details',
            'servicio',
            'servicio_details'
        ]
        # `usuario` lo maneja el servidor (se asigna desde request.user); evitar que el cliente lo envíe
        read_only_fields = ['id', 'fecha', 'usuario_details', 'servicio_details', 'usuario']
    def validate_autor(self, value):
        """
        Validar el nombre del autor de la reseña.
        """
        if not value or value.strip() == '':
            raise serializers.ValidationError("El nombre del autor no puede estar vacío")
        if len(value) < 2:
            raise serializers.ValidationError("El nombre del autor debe tener al menos 2 caracteres")
        if len(value) > 200:
            raise serializers.ValidationError("El nombre del autor no puede exceder 200 caracteres")
        
        # Verificar que solo contenga caracteres válidos para nombres
        if not all(char.isalpha() or char.isspace() for char in value):
            raise serializers.ValidationError(
                "El nombre del autor solo puede contener letras y espacios"
            )
        
        return value.strip()
    
    def validate_destino(self, value):
        """
        Validar el nombre del destino reseñado.
        """
        if not value or value.strip() == '':
            raise serializers.ValidationError("El destino no puede estar vacío")
        if len(value) < 3:
            raise serializers.ValidationError("El destino debe tener al menos 3 caracteres")
        if len(value) > 300:
            raise serializers.ValidationError("El destino no puede exceder 300 caracteres")
        return value.strip()
    
    def validate_mensaje(self, value):
        """
        Validar el contenido del mensaje de la reseña.
        """
        if not value or value.strip() == '':
            raise serializers.ValidationError("El mensaje de la reseña no puede estar vacío")
        if len(value) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres")
        if len(value) > 1000:
            raise serializers.ValidationError("El mensaje no puede exceder 1000 caracteres")
        return value.strip()
    
    def validate_calificacion(self, value):
        """
        Validar que la calificación esté entre 1 y 5 estrellas.
        """
        if not isinstance(value, int):
            raise serializers.ValidationError("La calificación debe ser un número entero")
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "La calificación debe estar entre 1 y 5 estrellas"
            )
        return value
    
    def validate(self, attrs):
        """
        Validación a nivel de objeto para verificar la consistencia de los datos.
        """
        # Verificar que si se proporciona un servicio, el destino coincida
        if 'servicio' in attrs and attrs['servicio']:
            servicio = attrs['servicio']
            if servicio.tipo_servicio == 'hotel':
                if hasattr(servicio, 'hotel'):
                    if attrs['destino'].lower() != servicio.hotel.nombre_lugar.lower():
                        raise serializers.ValidationError({
                            'destino': 'El destino debe coincidir con el nombre del hotel'
                        })
            elif servicio.tipo_servicio == 'restaurante':
                if hasattr(servicio, 'restaurante'):
                    if attrs['destino'].lower() != servicio.restaurante.nombre_lugar.lower():
                        raise serializers.ValidationError({
                            'destino': 'El destino debe coincidir con el nombre del restaurante'
                        })
        
        return attrs
    
    def create(self, validated_data):
        """
        Crear una nueva reseña asegurando que el autor coincida con el nombre del usuario.
        """
        # Asegurar que el autor coincida con el nombre del usuario
        usuario = validated_data.get('usuario')
        if usuario:
            validated_data['autor'] = usuario.nombre
        
        fotos = self.context.get('fotos') or []
        resena = super().create(validated_data)
        # Guardar fotos relacionadas si vienen en el contexto (manejo desde la view)
        for f in fotos:
            FotoResena.objects.create(resena=resena, imagen=f) #pylint: disable=no-member
        return resena