from django.db import models


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
        return f'FotoResena {self.pk} para {self.resena}'


