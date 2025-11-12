from django.db import models
from servicios.models.servicio import Servicio

class Atraccion(Servicio):
    nombre_lugar = models.CharField(max_length=200)

    
    class Meta:
        db_table = 'atracciones'
        verbose_name = 'Atracción'
        verbose_name_plural = 'Atracciones'
    
    def mostrar_tipo(self):
        print(f'🎡 Atracción turística: {self.nombre_lugar}')