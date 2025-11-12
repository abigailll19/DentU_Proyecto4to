from usuarios.models.usuario import Usuario


class Administrador(Usuario):
    """Administrador hereda los campos básicos de Usuario (nombre, correo, contrasena, etc.).

    No redeclaramos esos campos aquí para evitar colisiones. Añadir sólo campos
    adicionales específicos del administrador si se requieren.
    """

    class Meta:
        db_table = 'administradores'
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        # usa el campo `nombre` heredado de Usuario
        return str(self.nombre)

    # Métodos equivalentes
    def gestionar_usuario(self):
        print('Gestionando usuarios...')

    def eliminar_contenido(self):
        print('Eliminando contenido...')

