from django.urls import path, include
from rest_framework.routers import DefaultRouter
from resena.views.resenaViewSet import ResenaViewSet
from resena.views.foto_resena_viewset import FotoResenaViewSet

router = DefaultRouter()
router.register(r'resena', ResenaViewSet, basename='resena')
router.register(r'fotos-resena', FotoResenaViewSet, basename='fotos-resena')

urlpatterns = [
    path('', include(router.urls)),
]
