# usuarios/views/turista_viewset.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from usuarios.serializers.turista_serializer import TuristaSerializer
from usuarios.services import turista_service as service
from usuarios.permissions import IsAdminOrPropietario


class TuristaViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrPropietario]
    """
    Equivalente al TuristaController de NestJS.
    Llama a turista_service.py para la lógica de negocio.
    """

    def list(self, _request):
        """GET /turista/"""
        turistas = service.find_all_turistas()
        serializer = TuristaSerializer(turistas, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /turista/{id}/"""
        turista = service.find_one_turista(pk)
        serializer = TuristaSerializer(turista)
        return Response(serializer.data)

    def create(self, request):
        """POST /turista/"""
        turista = service.create_turista(request.data)
        serializer = TuristaSerializer(turista)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /turista/{id}/"""
        turista = service.update_turista(pk, request.data)
        serializer = TuristaSerializer(turista)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /turista/{id}/"""
        service.remove_turista(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
