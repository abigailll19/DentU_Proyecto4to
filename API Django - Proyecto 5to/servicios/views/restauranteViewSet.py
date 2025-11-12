from rest_framework import viewsets, status
from rest_framework.response import Response
from servicios.serializers.restaurante_serializer import RestauranteSerializer
from servicios.services.restaurante_service import RestauranteService


class RestauranteViewSet(viewsets.ViewSet):
    """
    Equivalente al RestauranteController de NestJS.
    """

    def list(self, _request):
        restaurantes = RestauranteService.find_all()
        serializer = RestauranteSerializer(restaurantes, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        restaurante = RestauranteService.find_one(pk)
        serializer = RestauranteSerializer(restaurante)
        return Response(serializer.data)

    def create(self, request):
        serializer = RestauranteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurante = RestauranteService.create(serializer.validated_data)
        return Response(RestauranteSerializer(restaurante).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        restaurante = RestauranteService.update(pk, request.data)
        serializer = RestauranteSerializer(restaurante)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        RestauranteService.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
