from django.db import models
from servicios.models.lugaresTuristicos import LugaresTuristico


class Restaurante(LugaresTuristico):
    tipoComida = models.CharField(max_length=255)
    # propietario se hereda desde Servicio -> LugaresTuristico, no duplicar el campo aquí
    
    class Meta:
        db_table = 'restaurantes'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
    
    def publicar_menu(self):
        print(f'📜 Menú del restaurante de comida {self.tipoComida}')