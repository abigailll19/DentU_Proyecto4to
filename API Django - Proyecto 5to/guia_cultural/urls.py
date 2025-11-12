from django.urls import path, include
from rest_framework.routers import DefaultRouter
from guia_cultural.guia_culturalViewSet import GuiaCulturalViewSet

router = DefaultRouter()
router.register(r'guia-cultural', GuiaCulturalViewSet, basename='guia-cultural')

urlpatterns = [
    path('', include(router.urls)),
]
