# usuarios/services/usuario_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from usuarios.models import Usuario
from usuarios.serializers.usuario_serializer import UsuarioSerializer
from usuarios.signals import crear_usuario_con_tipo


def create_user(data):
    """Crea un Usuario del tipo correcto según el campo 'tipo'."""
    # Si viene tipo específico, crear en tabla especializada
    tipo = data.get('tipo', '')
    if tipo in ['turista', 'propietario', 'administrador', 'admin']:
        return crear_usuario_con_tipo(
            nombre=data.get('nombre'),
            correo=data.get('correo'),
            contrasena=data.get('contrasena'),
            tipo=tipo,
            idiomaPreferido=data.get('idiomaPreferido', 'es')
        )
    else:
        # Crear usuario base normal
        serializer = UsuarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()


def find_all_users():
    """Devuelve QuerySet de todos los usuarios."""
    return Usuario.objects.all()  # pylint: disable=no-member


def find_one_user(pk):
    """Devuelve un usuario o lanza 404."""
    return get_object_or_404(Usuario, pk=pk)


@transaction.atomic
def update_user(pk, data):
    """Actualiza parcialmente un usuario (usa partial=True para PATCH)."""
    instance = get_object_or_404(Usuario, pk=pk)
    serializer = UsuarioSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def remove_user(pk):
    """Elimina el usuario (lanza 404 si no existe)."""
    instance = get_object_or_404(Usuario, pk=pk)
    instance.delete()
