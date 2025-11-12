from django.shortcuts import get_object_or_404
from django.db import transaction
from servicios.models.restaurante import Restaurante
from servicios.serializers.restaurante_serializer import RestauranteSerializer


class RestauranteService:

    @staticmethod
    def find_all():
        return Restaurante.objects.all() #pylint: disable=E1101

    @staticmethod
    def find_one(id_restaurante):
        return get_object_or_404(Restaurante, id=id_restaurante)

    @staticmethod
    @transaction.atomic
    def create(data):
        serializer = RestauranteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    @transaction.atomic
    def update(id_restaurante, data):
        restaurante = RestauranteService.find_one(id_restaurante)
        serializer = RestauranteSerializer(restaurante, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    @transaction.atomic
    def remove(id_restaurante):
        restaurante = RestauranteService.find_one(id_restaurante)
        restaurante.delete()
