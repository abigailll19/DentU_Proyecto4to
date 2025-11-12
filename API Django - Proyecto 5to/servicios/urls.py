from django.urls import path, include
from rest_framework.routers import DefaultRouter
from servicios.views.atraccionViewSet import AtraccionViewSet
from servicios.views.hotelViewSet import HotelViewSet
from servicios.views.lugaresturisticosViewSet import LugaresTuristicosViewSet
from servicios.views.mediotransporteViewSet import MedioTransporteViewSet
from servicios.views.restauranteViewSet import RestauranteViewSet
from servicios.views.servicioViewSet import ServicioViewSet
from servicios.views.visitaViewSet import VisitaViewSet
from servicios.views.foto_lugar_viewset import FotoLugarViewSet

router = DefaultRouter()
router.register(r'atraccion', AtraccionViewSet, basename='atraccion')
router.register(r'hotel', HotelViewSet, basename='hotel')
router.register(r'lugares-turisticos', LugaresTuristicosViewSet, basename='lugares-turisticos')
router.register(r'medio-transporte', MedioTransporteViewSet, basename='medio-transporte')
router.register(r'restaurante', RestauranteViewSet, basename='restaurante')
router.register(r'servicio', ServicioViewSet, basename='servicio')
router.register(r'visitas', VisitaViewSet, basename='visitas')
router.register(r'fotos-lugar', FotoLugarViewSet, basename='fotos-lugar')
urlpatterns = [
    path('', include(router.urls)),
]
