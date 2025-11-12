# tu_app/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .guia_cultural_service import (
    create_guia,
    find_all_guias,
    find_one_guia,
    update_guia,
    remove_guia,
)
from .serializers import GuiaCulturalSerializer

class GuiaCulturalViewSet(viewsets.ViewSet):
    """
    Equivalente al GuiaCulturalController de NestJS.
    Este ViewSet llama al service para la lógica de negocio.
    """

    def list(self, _request):
        """GET /guia-cultural/"""
        qs = find_all_guias()
        serializer = GuiaCulturalSerializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        """GET /guia-cultural/{id}/"""
        obj = find_one_guia(pk)
        serializer = GuiaCulturalSerializer(obj)
        return Response(serializer.data)

    def create(self, request):
        """POST /guia-cultural/"""
        obj = create_guia(request.data)
        serializer = GuiaCulturalSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """PATCH /guia-cultural/{id}/"""
        obj = update_guia(pk, request.data)
        serializer = GuiaCulturalSerializer(obj)
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        """DELETE /guia-cultural/{id}/"""
        remove_guia(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
