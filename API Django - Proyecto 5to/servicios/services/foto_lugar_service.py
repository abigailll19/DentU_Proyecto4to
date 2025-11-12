from django.shortcuts import get_object_or_404
from servicios.models.foto_lugar import FotoLugar
from servicios.models.lugaresTuristicos import LugaresTuristico


class FotoLugarService:
    @staticmethod
    def list_by_lugar(lugar_pk):
        lugar = get_object_or_404(LugaresTuristico, pk=lugar_pk)
        return FotoLugar.objects.filter(lugar=lugar) #pylint: disable=no-member

    @staticmethod
    def create(lugar_pk, imagen, descripcion=None):
        lugar = get_object_or_404(LugaresTuristico, pk=lugar_pk)
        foto = FotoLugar.objects.create(lugar=lugar, imagen=imagen, descripcion=descripcion) #pylint: disable=no-member
        return foto

    @staticmethod
    def bulk_create(lugar_pk, imagenes):
        lugar = get_object_or_404(LugaresTuristico, pk=lugar_pk)
        fotos = []
        for img in imagenes:
            fotos.append(FotoLugar.objects.create(lugar=lugar, imagen=img)) #pylint: disable=no-member
        return fotos

    @staticmethod
    def remove(pk):
        foto = get_object_or_404(FotoLugar, pk=pk)
        foto.delete()
        return None
