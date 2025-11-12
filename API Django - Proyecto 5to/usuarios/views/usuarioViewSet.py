from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from usuarios.models import Usuario
from usuarios.serializers.usuario_serializer import UsuarioSerializer
from usuarios.services import usuarios_service as user_service
from usuarios.permissions import IsAdministrador


class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdministrador]
    """
    ViewSet para Usuario que delega la lógica al usuario_service.
    """
    queryset = Usuario.objects.all()  # pylint: disable=no-member
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        user = user_service.create_user(request.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        qs = user_service.find_all_users()
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = user_service.find_one_user(pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = user_service.update_user(pk, request.data)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_service.remove_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)