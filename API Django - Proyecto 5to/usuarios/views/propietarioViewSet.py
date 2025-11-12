# usuarios/views/propietario_viewset.py

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response

from usuarios.serializers.propietario_serializer import PropietarioSerializer
from usuarios.services import propietario_service as service
from usuarios.permissions import IsAdminOrPropietario


class PropietarioViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrPropietario]
    """
    Equivalente directo al PropietarioController de NestJS.
    Este ViewSet llama al service (lógica de negocio).
    """

    def list(self, _request):
        """GET /propietario/"""
        propietarios = service.find_all_propietarios()
        serializer = PropietarioSerializer(propietarios, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /propietario/{id}/"""
        propietario = service.find_one_propietario(pk)
        serializer = PropietarioSerializer(propietario)
        return Response(serializer.data)

    def create(self, request):
        """POST /propietario/"""
        propietario = service.create_propietario(request.data)
        serializer = PropietarioSerializer(propietario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /propietario/{id}/"""
        propietario = service.update_propietario(pk, request.data)
        serializer = PropietarioSerializer(propietario)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /propietario/{id}/"""
        service.remove_propietario(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
