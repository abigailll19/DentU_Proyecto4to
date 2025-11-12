from django.shortcuts import get_object_or_404
from servicios.models.servicio import Servicio


class ServicioService:

    @staticmethod
    def find_all():
        return Servicio.objects.all() #pylint: disable=no-member

    @staticmethod
    def find_one(id_servicio):
        return get_object_or_404(Servicio, id=id_servicio)

    @staticmethod
    def create(data):
        return Servicio.objects.create(**data) #pylint: disable=no-member

    @staticmethod
    def update(id_servicio, data):
        servicio = ServicioService.find_one(id_servicio)
        for field, value in data.items():
            setattr(servicio, field, value)
        servicio.save()
        return servicio

    @staticmethod
    def remove(id_servicio):
        servicio = ServicioService.find_one(id_servicio)
        servicio.delete()
