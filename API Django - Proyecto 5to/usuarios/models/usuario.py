from django.db import models


class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)  # Usar Django Auth en producción
    tipo = models.CharField(max_length=50)
    idiomaPreferido = models.CharField(max_length=10, default='es')
    
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
        
        