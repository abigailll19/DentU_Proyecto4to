# servicios/models/hotel.py
from django.db import models
from servicios.models.lugaresTuristicos import LugaresTuristico

class Hotel(LugaresTuristico):
    clasificacion = models.CharField(max_length=255)
    servicios_hotel = models.CharField(max_length=255)
    # propietario se hereda desde Servicio -> LugaresTuristico, no duplicar el campo aquí

    class Meta:
        db_table = 'hoteles'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'

    def mostrar_servicios(self):
        print(f'🛎️ Servicios del hotel: {self.servicios_hotel}')
