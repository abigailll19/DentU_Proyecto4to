from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import GuiaCultural
from .serializers import GuiaCulturalSerializer


def create_guia(data):
    """Crea una guía cultural validando con el serializer."""
    serializer = GuiaCulturalSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def find_all_guias():
    """Devuelve queryset con todas las guías."""
    return GuiaCultural.objects.all() #pylint: disable=no-member

def find_one_guia(pk):
    """Devuelve una guía o lanza 404."""
    return get_object_or_404(GuiaCultural, pk=pk)

@transaction.atomic
def update_guia(pk, data):
    """Actualiza parcialmente (PATCH)."""
    instance = get_object_or_404(GuiaCultural, pk=pk)
    serializer = GuiaCulturalSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

@transaction.atomic
def remove_guia(pk):
    """Elimina la guía."""
    instance = get_object_or_404(GuiaCultural, pk=pk)
    instance.delete()
