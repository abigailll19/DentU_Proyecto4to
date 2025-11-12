from rest_framework import serializers
from resena.models import FotoResena


class FotoResenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoResena
        fields = ['id', 'imagen', 'descripcion']
        read_only_fields = ['id']
