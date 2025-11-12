from django.shortcuts import get_object_or_404
from resena.models import Resena, FotoResena


class ResenaService:
    """
    Service encargado de la lógica de negocio de Reseñas.
    """

    def create(self, data, fotos=None):
        fotos = fotos or []
        # Si se recibe usuario en data ya está listo
        resena = Resena.objects.create(**data) #pylint: disable=no-member
        for f in fotos:
            FotoResena.objects.create(resena=resena, imagen=f) #pylint: disable=no-member
        return resena

    def find_all(self):
        return Resena.objects.all() #pylint: disable=no-member

    def find_one(self, id_resena):
        return get_object_or_404(Resena, id=id_resena)

    def update(self, id_resena, data):
        resena = self.find_one(id_resena)
        for key, value in data.items():
            setattr(resena, key, value)
        resena.save()
        return resena

    def remove(self, id_resena):
        resena = self.find_one(id_resena)
        resena.delete()
