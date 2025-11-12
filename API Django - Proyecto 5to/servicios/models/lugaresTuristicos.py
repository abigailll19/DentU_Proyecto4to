from django.db import models
from servicios.models.servicio import Servicio
from servicios.models.foto_lugar import FotoLugar

class LugaresTuristico(Servicio):
    nombre_lugar = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'lugares_turisticos'
        verbose_name = 'Lugar Turístico'
        verbose_name_plural = 'Lugares Turísticos'
    
    def __str__(self):
        return str(self.nombre_lugar)
    
    def mostrar_informacion(self):
        print(f'📍 {self.nombre_lugar} - {self.descripcion}')
    
    def ver_ubicacion(self):
        print(f'🗺️ Ubicación: {self.ubicacion}')

    def add_foto(self, imagen, descripcion=None):
        """Convenience helper para añadir una foto al lugar."""
        return FotoLugar.objects.create(lugar=self, imagen=imagen, descripcion=descripcion) #pylint: disable=no-member
        