"""
para que tipo_usuario se cree en la tabla de base de datos correcta segun rol
"""
from .models import Usuario, Administrador, Propietario, Turista


def crear_usuario_con_tipo(nombre, correo, contrasena, tipo, **kwargs):
    """
    Crea un usuario directamente en la tabla especializada según su tipo
    """
    datos_base = {
        'nombre': nombre,
        'correo': correo, 
        'contrasena': contrasena,
        'tipo': tipo,
        'idiomaPreferido': kwargs.get('idiomaPreferido', 'es')
    }
    
    if tipo == 'administrador' or tipo == 'admin':
        return Administrador.objects.create(**datos_base) #pylint: disable=no-member
    
    elif tipo == 'propietario':
        return Propietario.objects.create( #pylint: disable=no-member
            **datos_base,
            tipo_negocio=kwargs.get('tipo_negocio', 'Por definir')
        )
    
    elif tipo == 'turista':
        return Turista.objects.create( #pylint: disable=no-member
            **datos_base,
            preferencias=kwargs.get('preferencias', [])
        )
    
    else:
        # Si no es un tipo específico, crear Usuario base
        return Usuario.objects.create(**datos_base) #pylint: disable=no-member