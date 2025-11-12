from django.shortcuts import get_object_or_404
from servicios.models.mediotransporte import MedioTransporte
from servicios.models.lugaresTuristicos import LugaresTuristico
from django.db.models import Q

class MedioTransporteService:

    @staticmethod
    def find_all():
        return MedioTransporte.objects.all() #pylint: disable=no-member

    @staticmethod
    def find_one(id_transporte):
        return get_object_or_404(MedioTransporte, id_transporte=id_transporte)

    @staticmethod
    def create(data):
        return MedioTransporte.objects.create(**data) #pylint: disable=no-member

    @staticmethod
    def update(id_transporte, data):
        medio = MedioTransporteService.find_one(id_transporte)
        for key, value in data.items():
            setattr(medio, key, value)
        medio.save()
        return medio

    @staticmethod
    def remove(id_transporte):
        medio = MedioTransporteService.find_one(id_transporte)
        medio.delete()

    @staticmethod
    def find_by_lugar(lugar_pk):
        """Heurístico simple: busca medios cuyo campo `ruta` contenga el nombre o la ubicación del lugar."""
        lugar = get_object_or_404(LugaresTuristico, pk=lugar_pk)
        nombre = (lugar.nombre_lugar or '').strip()
        ubicacion = (getattr(lugar, 'ubicacion', '') or '').strip()
        # Buscar coincidencias en la ruta (case-insensitive) por nombre o por ubicacion
        q = Q()
        if nombre:
            q |= Q(ruta__icontains=nombre)
        if ubicacion:
            q |= Q(ruta__icontains=ubicacion)
        if q:
            return MedioTransporte.objects.filter(q)  #pylint: disable=no-member
        # fallback: devolver todos si no hay términos
        return MedioTransporte.objects.all()  #pylint: disable=no-member
