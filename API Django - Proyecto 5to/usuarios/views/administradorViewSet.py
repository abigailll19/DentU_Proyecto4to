from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from usuarios.serializers.administrador_serializer import AdministradorSerializer
from usuarios.services import administrador_service as service
from usuarios.permissions import IsAdministrador


class AdministradorViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    """
    Equivalente al AdministradorController de NestJS.
    Este ViewSet llama al administrador_service para la lógica de negocio.
    """

    def list(self, _request):
        """GET /administrador/"""
        admins = service.find_all_admins()
        serializer = AdministradorSerializer(admins, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /administrador/{id}/"""
        admin = service.find_one_admin(pk)
        serializer = AdministradorSerializer(admin)
        return Response(serializer.data)

    def create(self, request):
        """POST /administrador/"""
        admin = service.create_admin(request.data)
        serializer = AdministradorSerializer(admin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /administrador/{id}/"""
        admin = service.update_admin(pk, request.data)
        serializer = AdministradorSerializer(admin)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /administrador/{id}/"""
        service.remove_admin(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
