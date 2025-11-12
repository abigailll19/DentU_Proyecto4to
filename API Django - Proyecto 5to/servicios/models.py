from django.db import models
import uuid


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


class Visita(models.Model):
    """Marca simple que indica que un usuario marcará que irá a un servicio.

    Este modelo no es una señal de reserva; permite al propietario ver quién dijo que vendrá.
    """
    ESTADO_CHOICES = [
        ('ira', 'Irá'),
        ('no_ira', 'No irá'),
        ('cancelado', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='visitas'
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
        return f'{self.usuario} -> {self.servicio} ({self.estado})'

class LugaresTuristico(Servicio):
    nombre_lugar = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'lugares_turisticos'
        verbose_name = 'Lugar Turístico'
        verbose_name_plural = 'Lugares Turísticos'
    
    def __str__(self):
        return str(self.nombre_lugar)
    
    def mostrar_informacion(self):
        print(f'📍 {self.nombre_lugar} - {self.descripcion}')
    
    def ver_ubicacion(self):
        print(f'🗺️ Ubicación: {self.ubicacion}')
        
        
class Atraccion(Servicio):
    nombre_lugar = models.CharField(max_length=200)

    
    class Meta:
        db_table = 'atracciones'
        verbose_name = 'Atracción'
        verbose_name_plural = 'Atracciones'
    
    def mostrar_tipo(self):
        print(f'🎡 Atracción turística: {self.nombre_lugar}')
        

class Hotel(LugaresTuristico):
    clasificacion = models.CharField(max_length=255)
    servicios_hotel = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'hoteles'
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hoteles'
    
    def mostrar_servicios(self):
        print(f'🛎️ Servicios del hotel: {self.servicios_hotel}')
        

class Restaurante(LugaresTuristico):
    tipoComida = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'restaurantes'
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
    
    def publicar_menu(self):
        print(f'📜 Menú del restaurante de comida {self.tipoComida}')


class MedioTransporte(Servicio):
    id_transporte = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    


