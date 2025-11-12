from rest_framework import viewsets, status
from rest_framework.response import Response

from servicios.serializers.servicio_serializer import ServicioSerializer
from servicios.services.servicio_service import ServicioService


class ServicioViewSet(viewsets.ViewSet):
    """
    Equivalente al ServicioController de NestJS.
    """

    def list(self, _request):
        servicios = ServicioService.find_all()
        serializer = ServicioSerializer(servicios, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        servicio = ServicioService.find_one(pk)
        serializer = ServicioSerializer(servicio)
        return Response(serializer.data)

    def create(self, request):
        serializer = ServicioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        servicio = ServicioService.create(serializer.validated_data)
        return Response(ServicioSerializer(servicio).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        servicio = ServicioService.update(pk, request.data)
        serializer = ServicioSerializer(servicio)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        ServicioService.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
