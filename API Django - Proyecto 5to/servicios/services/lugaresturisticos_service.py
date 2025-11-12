# services/lugares_turisticos_service.py
from django.shortcuts import get_object_or_404
from servicios.models.lugaresTuristicos import LugaresTuristico
from servicios.models.foto_lugar import FotoLugar

class LugaresTuristicosService:

    @staticmethod
    def create(data):
        fotos = data.pop('fotos', None)
        lugar = LugaresTuristico.objects.create(**data) #pylint: disable=no-member
        # fotos puede ser una lista de InMemoryUploadedFile
        if fotos:
            for f in fotos:
                FotoLugar.objects.create(lugar=lugar, imagen=f) #pylint: disable=no-member
        return lugar

    @staticmethod
    def find_all():
        return LugaresTuristico.objects.all()  #pylint: disable=no-member

    @staticmethod
    def find_one(pk):
        return get_object_or_404(LugaresTuristico, pk=pk)

    @staticmethod
    def update(pk, data):
        lugar = get_object_or_404(LugaresTuristico, pk=pk)
        for key, value in data.items():
            setattr(lugar, key, value)
        lugar.save()
        return lugar

    @staticmethod
    def remove(pk):
        lugar = get_object_or_404(LugaresTuristico, pk=pk)
        lugar.delete()
