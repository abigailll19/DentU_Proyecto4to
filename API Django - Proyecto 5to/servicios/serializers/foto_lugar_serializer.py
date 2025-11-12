from rest_framework import serializers
from servicios.models.foto_lugar import FotoLugar


class FotoLugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoLugar
        fields = ['id', 'imagen', 'descripcion']
        read_only_fields = ['id']
