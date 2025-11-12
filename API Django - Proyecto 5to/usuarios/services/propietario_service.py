from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib.auth.hashers import make_password

from usuarios.models.propietario import Propietario
from usuarios.serializers.propietario_serializer import PropietarioSerializer


def create_propietario(data):
    """Crea un Propietario usando el serializer (valida y guarda)."""
    serializer = PropietarioSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def find_all_propietarios():
    """Devuelve QuerySet de todos los propietarios."""
    return Propietario.objects.all()  # pylint: disable=no-member


def find_one_propietario(pk):
    """Devuelve un propietario o lanza 404."""
    return get_object_or_404(Propietario, pk=pk)


@transaction.atomic
def update_propietario(pk, data):
    """Actualiza parcialmente un propietario (partial=True para PATCH)."""
    instance = get_object_or_404(Propietario, pk=pk)

    # Si viene contraseña, hashearla antes (porque el serializer sólo maneja create)
    if 'contrasena' in data and data['contrasena']:
        data = dict(data)  # copiar dict inmutable de request.data si viene QueryDict
        data['contrasena'] = make_password(data['contrasena'])

    serializer = PropietarioSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def remove_propietario(pk):
    """Elimina el propietario (lanza 404 si no existe)."""
    instance = get_object_or_404(Propietario, pk=pk)
    instance.delete()
