from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from servicios.serializers.foto_lugar_serializer import FotoLugarSerializer
from servicios.services.foto_lugar_service import FotoLugarService
from servicios.models.lugaresTuristicos import LugaresTuristico
from usuarios.permissions import IsOwnerOfLugarOrAdmin

service = FotoLugarService()


class FotoLugarViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOfLugarOrAdmin]

    def list(self, request):
        lugar_pk = request.query_params.get('lugar')
        if not lugar_pk:
            return Response({'detail': 'Se requiere parámetro `lugar`'}, status=status.HTTP_400_BAD_REQUEST)
        fotos = service.list_by_lugar(lugar_pk)
        serializer = FotoLugarSerializer(fotos, many=True)
        return Response(serializer.data)

    def create(self, request):
        lugar_pk = request.data.get('lugar') or request.query_params.get('lugar')
        if not lugar_pk:
            return Response({'detail': 'Se requiere campo `lugar`'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el lugar para validar permiso usando IsOwnerOfLugarOrAdmin
        try:
            lugar = LugaresTuristico.objects.get(pk=lugar_pk) #pylint: disable=no-member
        except LugaresTuristico.DoesNotExist:  #pylint: disable=no-member
            return Response({'detail': 'Lugar no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Crear un objeto dummy para check_object_permissions (lugar contenido)
        class DummyFotoLugar:
            def __init__(self, lugar):
                self.lugar = lugar
        
        dummy_foto = DummyFotoLugar(lugar)
        self.check_object_permissions(request, dummy_foto)

        # Aceptar una o varias imágenes con campo 'imagenes' o 'imagen'
        imagenes = []
        if 'imagenes' in request.FILES:
            imagenes = request.FILES.getlist('imagenes')
        elif 'imagen' in request.FILES:
            imagenes = [request.FILES.get('imagen')]
        else:
            return Response({'detail': 'Se requiere archivo de imagen en el campo `imagen` o `imagenes`'}, status=status.HTTP_400_BAD_REQUEST)

        fotos = service.bulk_create(lugar_pk, imagenes)
        serializer = FotoLugarSerializer(fotos, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        from servicios.models.foto_lugar import FotoLugar
        foto = FotoLugar.objects.filter(pk=pk).first() #pylint: disable=no-member
        if not foto:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        # Verificar permisos usando IsOwnerOfLugarOrAdmin a nivel de objeto
        self.check_object_permissions(request, foto)

        service.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
