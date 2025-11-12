from django.db import models
from usuarios.models.usuario import Usuario
from servicios.models import Servicio

class Resena(models.Model):
    # Autor puede ser nulo temporalmente durante migraciones; se poblará desde la relación con Usuario
    autor = models.CharField(max_length=200)
    destino = models.CharField(max_length=300)  # Lugar o servicio reseñado
    mensaje = models.TextField()
    calificacion = models.IntegerField(default=5)  # 1 a 5 estrellas
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Relación con Usuario
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='resenas'
    )
    
    # Relación con Servicio
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='resenas',
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'resenas'
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-fecha']
    
    def __str__(self):
        return f'{self.autor} - {self.destino} ({self.calificacion}★)'

class FotoResena(models.Model):
    resena = models.ForeignKey(
        'resena.Resena',
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    imagen = models.ImageField(upload_to='resenas/')
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'fotos_resena'
        verbose_name = 'Foto Reseña'
        verbose_name_plural = 'Fotos de Reseñas'

    def __str__(self):
        return f'FotoResena {self.pk or "nuevo"} para {self.resena}'