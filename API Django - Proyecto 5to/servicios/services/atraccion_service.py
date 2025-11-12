# servicios/services/atraccion_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from servicios.models.atraccion import Atraccion
from servicios.serializers.atraccion_serializer import AtraccionSerializer


def create_atraccion(data):
    """Crea una atracción usando el serializer."""
    serializer = AtraccionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def find_all_atracciones():
    """Retorna todas las atracciones."""
    return Atraccion.objects.all() # pylint: disable=no-member


def find_one_atraccion(pk):
    """Obtiene una atracción o lanza 404."""
    return get_object_or_404(Atraccion, pk=pk)


@transaction.atomic
def update_atraccion(pk, data):
    """Actualiza parcialmente una atracción."""
    instance = get_object_or_404(Atraccion, pk=pk)
    serializer = AtraccionSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def remove_atraccion(pk):
    """Elimina una atracción."""
    instance = get_object_or_404(Atraccion, pk=pk)
    instance.delete()
