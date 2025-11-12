# servicios/views/hotel_viewset.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from servicios.serializers.hotel_serializer import HotelSerializer
from servicios.services import hotel_service as service


class HotelViewSet(viewsets.ViewSet):
    """
    Equivalente a HotelController de NestJS.
    Toda la lógica delegada al service.
    """

    def list(self, _request):
        """GET /hotel/"""
        hoteles = service.find_all_hoteles()
        serializer = HotelSerializer(hoteles, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /hotel/{id}/"""
        hotel = service.find_one_hotel(pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def create(self, request):
        """POST /hotel/"""
        hotel = service.create_hotel(request.data)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /hotel/{id}/"""
        hotel = service.update_hotel(pk, request.data)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /hotel/{id}/"""
        service.remove_hotel(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
