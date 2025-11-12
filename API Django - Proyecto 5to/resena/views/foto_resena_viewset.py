from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from resena.services.foto_resena_service import FotoResenaService
from resena.models import Resena, FotoResena
from resena.serializers import FotoResenaSerializer
from usuarios.permissions import IsOwnerOfResenaOrAdmin


service = FotoResenaService()


class FotoResenaViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOfResenaOrAdmin]

    def list(self, request):
        resena_pk = request.query_params.get('resena')
        if not resena_pk:
            return Response({'detail': 'Se requiere parámetro `resena`'}, status=status.HTTP_400_BAD_REQUEST)
        fotos = service.list_by_resena(resena_pk)
        serializer = FotoResenaSerializer(fotos, many=True)
        return Response(serializer.data)

    def create(self, request):
        resena_pk = request.data.get('resena') or request.query_params.get('resena')
        if not resena_pk:
            return Response({'detail': 'Se requiere campo `resena`'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que la reseña existe (la validación de permiso se hace en permission class)
        try:
            resena = Resena.objects.get(pk=resena_pk) #pylint: disable=no-member
        except Resena.DoesNotExist:  #pylint: disable=no-member
            return Response({'detail': 'Reseña no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos usando IsOwnerOfResenaOrAdmin a nivel de objeto
        self.check_object_permissions(request, resena)

        imagenes = []
        if 'imagenes' in request.FILES:
            imagenes = request.FILES.getlist('imagenes')
        elif 'imagen' in request.FILES:
            imagenes = [request.FILES.get('imagen')]
        else:
            return Response({'detail': 'Se requiere archivo de imagen en el campo `imagen` o `imagenes`'}, status=status.HTTP_400_BAD_REQUEST)

        fotos = service.bulk_create(resena_pk, imagenes)
        serializer = FotoResenaSerializer(fotos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        foto = FotoResena.objects.filter(pk=pk).first() #pylint: disable=no-member
        if not foto:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos usando IsOwnerOfResenaOrAdmin a nivel de objeto
        self.check_object_permissions(request, foto)

        service.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
