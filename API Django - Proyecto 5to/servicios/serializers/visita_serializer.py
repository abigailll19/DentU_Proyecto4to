from rest_framework import serializers
from servicios.models.visita import Visita
from servicios.models.servicio import Servicio

class VisitaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    servicio_id = serializers.PrimaryKeyRelatedField(
        queryset=Servicio.objects.all(), #pylint: disable=no-member
        source='servicio',
        write_only=True
    )
    servicio = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Visita
        fields = [
            'id',
            'servicio',        # solo lectura (nombre/string)
            'servicio_id',     # escritura (id)
            'usuario',
            'fecha_visita',
            'estado',
            'nota',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'usuario']

    def validate_servicio(self, servicio):
        # Validar solo restaurantes y hoteles
        if servicio.tipo not in ['restaurante', 'hotel']:
            raise serializers.ValidationError("Solo puedes marcar visitas a restaurantes u hoteles.")
        return servicio
