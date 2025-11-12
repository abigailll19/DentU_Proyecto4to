# usuarios/services/administrador_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from usuarios.models import Administrador
from usuarios.serializers.administrador_serializer import AdministradorSerializer

def create_admin(data):
    """Crea un Administrador usando el serializer (valida y guarda)."""
    serializer = AdministradorSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

def find_all_admins():
    """Devuelve QuerySet de todos los administradores."""
    return Administrador.objects.all() # pylint: disable=no-member

def find_one_admin(pk):
    """Devuelve un administrador o lanza 404."""
    return get_object_or_404(Administrador, pk=pk)

@transaction.atomic
def update_admin(pk, data):
    """Actualiza parcialmente un admin (usa partial=True para PATCH)."""
    instance = get_object_or_404(Administrador, pk=pk)
    serializer = AdministradorSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()

@transaction.atomic
def remove_admin(pk):
    """Elimina el admin (lanza 404 si no existe)."""
    instance = get_object_or_404(Administrador, pk=pk)
    instance.delete()
