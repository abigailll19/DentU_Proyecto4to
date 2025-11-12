# usuarios/services/turista_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from usuarios.models import Turista
from usuarios.serializers.turista_serializer import TuristaSerializer


def create_turista(data):
    """Crea un Turista usando el serializer (valida y guarda)."""
    serializer = TuristaSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def find_all_turistas():
    """Devuelve queryset de todos los turistas."""
    return Turista.objects.all()  # pylint: disable=no-member


def find_one_turista(pk):
    """Devuelve un turista o lanza 404."""
    return get_object_or_404(Turista, pk=pk)


@transaction.atomic
def update_turista(pk, data):
    """Actualiza parcialmente un turista."""
    instance = get_object_or_404(Turista, pk=pk)
    serializer = TuristaSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def remove_turista(pk):
    """Elimina el turista (404 si no existe)."""
    instance = get_object_or_404(Turista, pk=pk)
    instance.delete()
