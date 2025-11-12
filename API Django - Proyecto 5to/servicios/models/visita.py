from django.db import models
from servicios.models.lugaresTuristicos import LugaresTuristico



class Visita(models.Model):
    """Marca simple que indica que un usuario marcará que irá a un servicio.

    Este modelo no es una señal de reserva; permite al propietario ver quién dijo que vendrá.
    """
    ESTADO_CHOICES = [
        ('ira', 'Irá'),
        ('no_ira', 'No irá'),
        ('cancelado', 'Cancelado'),
    ]

    lugar = models.ForeignKey(
        LugaresTuristico,
        on_delete=models.CASCADE,
        related_name='visitas_lugar',
        null=True,
        blank=True
    )
    # Algunos visitantes marcan visitas a servicios (hoteles, restaurantes)
    # que están gestionados por un Propietario. Otros lugares (playas, miradores)
    # no tienen propietario y usan `lugar`.
    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='visitas_servicio'
    )
    usuario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='visitas'
    )
    fecha_visita = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ira')
    nota = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'visitas'
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-created_at']

    def __str__(self):
        objetivo = self.servicio if self.servicio else self.lugar
        return f'{self.usuario} visitará {objetivo} ({self.estado})'

    def get_propietario(self):
        """
        Devuelve el propietario asociado a esta visita si existe (solo para servicios).
        Retorna None si la visita es a un lugar turístico sin propietario.
        """
        if self.servicio and getattr(self.servicio, 'propietario', None):
            return self.servicio.propietario
        return None