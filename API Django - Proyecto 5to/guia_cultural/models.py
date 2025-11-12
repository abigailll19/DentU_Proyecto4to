from django.db import models


class GuiaCultural(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=100)
    # Ej: 'normas_culturales', 'frases_basicas', 'costumbres', 'etiqueta'
    contenido = models.TextField(null=True, blank=True)
    # Puede ser texto completo de la guía, instrucciones o frases útiles
    
    class Meta:
        db_table = 'guias_culturales'
        verbose_name = 'Guía Cultural'
        verbose_name_plural = 'Guías Culturales'
    
    def __str__(self):
        return str(self.titulo )
    
    