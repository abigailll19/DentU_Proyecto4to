from django.db import models


class FotoLugar(models.Model):
    lugar = models.ForeignKey(
        'servicios.LugaresTuristico',
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    imagen = models.ImageField(upload_to='lugares/')
    descripcion = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'fotos_lugar'
        verbose_name = 'Foto Lugar'
        verbose_name_plural = 'Fotos de Lugares'

    def __str__(self):
        return f'FotoLugar {self.pk or "nuevo"} para {self.lugar}'
