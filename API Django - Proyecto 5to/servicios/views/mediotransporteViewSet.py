from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from servicios.serializers.mediotransporte_serializer import MedioTransporteSerializer
from servicios.services.mediotransporte_service import MedioTransporteService

class MedioTransporteViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    """
    Equivalente al MedioTransporteController de NestJS.
    Lectura pública, escritura solo para usuarios autenticados.
    """

    def list(self, request):
        # Si se pasa ?lugar=<id> usamos un heurístico para devolver transportes cuya `ruta` contiene
        # el nombre o la ubicación del lugar
        lugar_pk = request.query_params.get('lugar')
        if lugar_pk:
            medios = MedioTransporteService.find_by_lugar(lugar_pk)
        else:
            medios = MedioTransporteService.find_all()
        serializer = MedioTransporteSerializer(medios, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        medio = MedioTransporteService.find_one(pk)
        serializer = MedioTransporteSerializer(medio)
        return Response(serializer.data)

    def create(self, request):
        serializer = MedioTransporteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medio = MedioTransporteService.create(serializer.validated_data)
        return Response(MedioTransporteSerializer(medio).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        medio = MedioTransporteService.update(pk, request.data)
        serializer = MedioTransporteSerializer(medio)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        MedioTransporteService.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
