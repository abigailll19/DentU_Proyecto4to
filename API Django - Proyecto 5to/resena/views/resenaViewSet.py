from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from resena.serializers import ResenaSerializer
from resena.services.resena_service import ResenaService

service = ResenaService()


class ResenaViewSet(viewsets.ViewSet):
    """
    ViewSet para gestión de reseñas con autenticación y vistas por rol.
    
    Endpoints:
    - GET ?view=tourist: Reseñas destacadas (calificación >= 3)
    - GET ?view=owner: Reseñas de lugares del propietario
    - GET ?view=simple: Vista simplificada (calificación y mensaje)
    - GET (default): Vista completa
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, _request):
        # OPCIÓN SIMPLE: Query parameter para vista específica
        view_type = _request.GET.get('view', 'full')
        resenas = service.find_all() #pylint: disable=no-member
        
        # Filtrar según view parameter
        if view_type == 'tourist':
            # Vista turista: solo reseñas públicas y mejor valoradas
            resenas = [r for r in resenas if getattr(r, 'calificacion', 0) >= 3]
            serializer = ResenaSerializer(resenas, many=True)
            return Response({
                'resenas': serializer.data,
                'vista': 'turista',
                'mensaje': 'Reseñas destacadas'
            })
        elif view_type == 'owner' and hasattr(_request.user, 'propietario'):
            # Vista propietario: solo reseñas de sus lugares/servicios
            resenas = [r for r in resenas if getattr(r.servicio, 'propietario', None) == _request.user]
            serializer = ResenaSerializer(resenas, many=True)
            return Response({
                'resenas_mis_lugares': serializer.data,
                'vista': 'propietario',
                'total': len(serializer.data)
            })
        elif view_type == 'simple':
            # Vista simple: solo calificación y mensaje
            simple_data = [{'calificacion': r.calificacion, 'mensaje': r.mensaje[:100]} for r in resenas]
            return Response({'resenas': simple_data, 'vista': 'simple'})
        
        # Vista completa (default)
        serializer = ResenaSerializer(resenas, many=True)
        return Response(serializer.data)

    def retrieve(self, _request, pk=None):
        resena = service.find_one(pk) #pylint: disable=no-member
        serializer = ResenaSerializer(resena)
        return Response(serializer.data)

    def create(self, request):
        # Manejar multipart/form-data con fotos: extraer archivos y pasarlos al serializer vía context
        fotos = request.FILES.getlist('fotos') if 'fotos' in request.FILES else []
        serializer = ResenaSerializer(data=request.data, context={'fotos': fotos})
        serializer.is_valid(raise_exception=True)
        # Asegurar que la reseña se asocie al usuario autenticado
        data_with_user = {**serializer.validated_data, 'usuario': request.user}
        # pasar fotos al servicio para persistir FotoResena
        resena = service.create(data_with_user, fotos=fotos) #pylint: disable=no-member
        return Response(ResenaSerializer(resena).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        serializer = ResenaSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        resena = service.update(pk, serializer.validated_data) #pylint: disable=no-member
        return Response(ResenaSerializer(resena).data)

    def destroy(self, _request, pk=None):
        service.remove(pk) #pylint: disable=no-member
        return Response(status=status.HTTP_204_NO_CONTENT)
