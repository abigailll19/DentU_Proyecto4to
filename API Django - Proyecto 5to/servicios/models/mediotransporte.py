from django.db import models
from servicios.models.servicio import Servicio

class MedioTransporte(Servicio):
    nombreEmpresa = models.CharField(max_length=150)
    tipo_transporte = models.CharField(max_length=100)
    # Ej: 'bus', 'taxi', 'metro', 'a_pie'
    nombreCooperativa = models.CharField(max_length=200, null=True, blank=True)
    ruta = models.TextField(null=True, blank=True)
    # Descripción de la ruta o trayecto
    tarifa = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distancia_km = models.IntegerField(null=True, blank=True)
    tiempo_estimado_min = models.IntegerField(null=True, blank=True)
    
    # Relación con Servicio (se define en el modelo Servicio con ForeignKey)
    
    class Meta:
        db_table = 'medios_transporte'
        verbose_name = 'Medio de Transporte'
        verbose_name_plural = 'Medios de Transporte'
    
    def __str__(self):
        return f'{self.nombreEmpresa} - {self.tipo_transporte}'
    

