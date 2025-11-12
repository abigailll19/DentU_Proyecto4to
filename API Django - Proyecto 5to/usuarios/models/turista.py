from django.db import models
from django.apps import apps
from .usuario import Usuario


class Turista(Usuario):
    # En Django, para arrays usamos JSONField o TextField con serialización
    preferencias = models.JSONField(default=list, blank=True)
    
    class Meta:
        db_table = 'turistas'
        verbose_name = 'Turista'
        verbose_name_plural = 'Turistas'
    
    def ver_lugares(self):
        print(f'{self.nombre} está viendo lugares turísticos.')
        return []
    
    def ver_restaurantes(self):
        print(f'{self.nombre} está viendo restaurantes.')
        return []
    
    def ver_transportes(self):
        print(f'{self.nombre} está viendo medios de transporte.')
        return []
    
    def ver_recomendaciones(self):
        print(f'{self.nombre} está viendo recomendaciones personalizadas.')
        return []
    
    def aplicar_filtros(self):
        print(f'{self.nombre} aplicó filtros de búsqueda.')
    
    def escribir_resena(self, resena):
        print(f'{self.nombre} escribió una reseña sobre {resena.destino}.')