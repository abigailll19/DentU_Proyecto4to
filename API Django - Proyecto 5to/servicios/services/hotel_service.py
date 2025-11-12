# servicios/services/hotel_service.py
from django.shortcuts import get_object_or_404
from django.db import transaction
from servicios.models.hotel import Hotel
from servicios.serializers.hotel_serializer import HotelSerializer


def create_hotel(data):
    serializer = HotelSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def find_all_hoteles():
    return Hotel.objects.all() #pylint: disable=no-member


def find_one_hotel(pk):
    return get_object_or_404(Hotel, pk=pk)


@transaction.atomic
def update_hotel(pk, data):
    instance = get_object_or_404(Hotel, pk=pk)
    serializer = HotelSerializer(instance, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


@transaction.atomic
def remove_hotel(pk):
    instance = get_object_or_404(Hotel, pk=pk)
    instance.delete()
