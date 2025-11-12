# servicios/views/atraccion_viewset.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from servicios.serializers.atraccion_serializer import AtraccionSerializer
from servicios.services import atraccion_service as service


class AtraccionViewSet(viewsets.ViewSet):
    """
    Equivalente a AtraccionController de NestJS.
    Delegamos toda la lógica al service.
    """

    def list(self, _request):
        """GET /atraccion/"""
        atracciones = service.find_all_atracciones()
        serializer = AtraccionSerializer(atracciones, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /atraccion/{id}/"""
        atraccion = service.find_one_atraccion(pk)
        serializer = AtraccionSerializer(atraccion)
        return Response(serializer.data)

    def create(self, request):
        """POST /atraccion/"""
        atraccion = service.create_atraccion(request.data)
        serializer = AtraccionSerializer(atraccion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /atraccion/{id}/"""
        atraccion = service.update_atraccion(pk, request.data)
        serializer = AtraccionSerializer(atraccion)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /atraccion/{id}/"""
        service.remove_atraccion(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
