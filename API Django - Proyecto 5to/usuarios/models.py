from django.db import models
import uuid


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)  # Usar Django Auth en producción
    tipo = models.CharField(max_length=50, blank=True)
    idiomaPreferido = models.CharField(max_length=10, default='es', choices=[
        ('es', 'Español'),
        ('en', 'English'),
        ('pt', 'Português')
    ])
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return str(self.nombre)
    
    def iniciar_sesion(self):
        print(f'{self.nombre} ha iniciado sesión.')
    
    def cerrar_sesion(self):
        print(f'{self.nombre} ha cerrado sesión.')
    
    def cambiar_idioma(self, nuevo_idioma):
        self.idiomaPreferido = nuevo_idioma
        self.save()
        print(f'{self.nombre} cambió el idioma a {self.idiomaPreferido}.')


class Propietario(Usuario):
    tipo_negocio = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'propietarios'
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'


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
        

class Administrador(Usuario):
    # No necesita campos extra, hereda todo de Usuario
    
    class Meta:
        db_table = 'administradores'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
    
    # Métodos equivalentes
    def gestionar_usuario(self):
        print('Gestionando usuarios...')
    
    def eliminar_contenido(self):
        print('Eliminando contenido...')

