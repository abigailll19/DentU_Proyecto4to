from django.urls import path, include
from rest_framework.routers import DefaultRouter
from usuarios.views.administradorViewSet import AdministradorViewSet
from usuarios.views.propietarioViewSet import PropietarioViewSet
from usuarios.views.turistaViewSet import TuristaViewSet
from usuarios.views.usuarioViewSet import UsuarioViewSet

router = DefaultRouter()
router.register(r'administrador', AdministradorViewSet, basename='administrador')
router.register(r'propietario', PropietarioViewSet, basename='propietario')
router.register(r'turista', TuristaViewSet, basename='turista')
router.register(r'usuario', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]
