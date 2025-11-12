from rest_framework import permissions


class IsAdministrador(permissions.BasePermission):
    """Usuario con rol administrador (o staff)"""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')))


class IsPropietario(permissions.BasePermission):
    """Usuario con rol propietario"""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'propietario'))


class IsTurista(permissions.BasePermission):
    """Usuario con rol turista"""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and hasattr(user, 'turista'))


class IsAdminOrPropietario(permissions.BasePermission):
    """Permite acceso si es administrador o propietario."""
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return bool(getattr(user, 'is_staff', False) or hasattr(user, 'administrador') or hasattr(user, 'propietario'))


class IsAdminOnly(permissions.BasePermission):
    """Solo administradores del sistema (o staff)."""
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')))


class EsPropietarioOPropioUsuario(permissions.BasePermission):
    """Object-level: propietario del servicio puede ver las visitas; el turista puede ver/editar su propia visita; admin lo ve todo."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Admin siempre
        if user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')):
            return True
        # Propietario del servicio
        if hasattr(obj, 'servicio') and hasattr(obj.servicio, 'propietario') and obj.servicio.propietario == user:
            return True
        # Usuario propietario de la visita
        return hasattr(obj, 'usuario') and obj.usuario == user


class IsOwnerOfResenaOrAdmin(permissions.BasePermission):
    """Object-level: solo el autor de la reseña o admin pueden crear/modificar fotos de esa reseña."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Admin siempre
        if user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')):
            return True
        # Owner de la reseña
        if hasattr(obj, 'resena') and hasattr(obj.resena, 'usuario') and obj.resena.usuario == user:
            return True
        # Si el objeto es la reseña directamente
        if hasattr(obj, 'usuario') and obj.usuario == user:
            return True
        return False


class IsOwnerOfLugarOrAdmin(permissions.BasePermission):
    """Object-level: solo el propietario del lugar o admin pueden crear/modificar fotos de ese lugar."""
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Admin siempre
        if user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')):
            return True
        # Propietario del lugar
        if hasattr(obj, 'lugar'):
            lugar = obj.lugar
            propietario_del_lugar = getattr(lugar, 'propietario', None)
            user_prop = getattr(user, 'propietario', None)
            return propietario_del_lugar == user or propietario_del_lugar == user_prop
        return False


class PropietarioSoloLectura(permissions.BasePermission):
    """Propietarios pueden VER pero NO EDITAR sus lugares/servicios."""
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        
        # Admin siempre puede todo
        if getattr(user, 'is_staff', False) or hasattr(user, 'administrador'):
            return True
            
        # Propietarios solo pueden leer (GET)
        if hasattr(user, 'propietario'):
            return request.method in permissions.SAFE_METHODS
            
        return False


class VisitasSoloLecturaPropietario(permissions.BasePermission):
    """Para visitas: propietarios solo leen, usuarios pueden editar las suyas."""
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        return True
        
    def has_object_permission(self, request, view, obj):
        user = request.user
        # Admin siempre
        if user and user.is_authenticated and (getattr(user, 'is_staff', False) or hasattr(user, 'administrador')):
            return True
            
        # Propietario del servicio: solo lectura 
        if hasattr(user, 'propietario') and hasattr(obj, 'servicio') and hasattr(obj.servicio, 'propietario'):
            if obj.servicio.propietario == user:
                return request.method in permissions.SAFE_METHODS
                
        # Usuario que hizo la visita: puede editarla
        if hasattr(obj, 'usuario') and obj.usuario == user:
            return True
            
        return False
