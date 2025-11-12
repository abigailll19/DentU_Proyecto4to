from django.shortcuts import get_object_or_404
from resena.models import FotoResena, Resena


class FotoResenaService:
    @staticmethod
    def list_by_resena(resena_pk):
        resena = get_object_or_404(Resena, pk=resena_pk)
        return FotoResena.objects.filter(resena=resena) #pylint: disable=no-member

    @staticmethod
    def create(resena_pk, imagen, descripcion=None):
        resena = get_object_or_404(Resena, pk=resena_pk)
        foto = FotoResena.objects.create(resena=resena, imagen=imagen, descripcion=descripcion) #pylint: disable=no-member
        return foto

    @staticmethod
    def bulk_create(resena_pk, imagenes):
        resena = get_object_or_404(Resena, pk=resena_pk)
        fotos = []
        for img in imagenes:
            fotos.append(FotoResena.objects.create(resena=resena, imagen=img)) #pylint: disable=no-member
        return fotos

    @staticmethod
    def remove(pk):
        foto = get_object_or_404(FotoResena, pk=pk)
        foto.delete()
        return None
