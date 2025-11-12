from django.db import models

class Servicio(models.Model):
    descripcion = models.CharField(max_length=200)
    tipo_servicio = models.CharField(max_length=100)
    horario = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Propietario del servicio (si aplica) - propietario que gestiona el negocio
    propietario = models.ForeignKey(
        'usuarios.Propietario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servicios_propios'
    )

    # Relación con MedioTransporte 
    medioTransporte = models.ForeignKey(
        'MedioTransporte',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servicios',
        db_column='id_transporte'
    )
    
    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
    
    def __str__(self):
        return f'{self.tipo_servicio} - {self.descripcion}'
