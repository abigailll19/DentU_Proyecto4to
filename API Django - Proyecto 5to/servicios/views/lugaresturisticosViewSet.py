# views/lugares_turisticos_viewset.py
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from servicios.serializers.lugaresturisticos_serializer import LugaresTuristicoSerializer
from servicios.services.lugaresturisticos_service import LugaresTuristicosService
from usuarios.permissions import IsAdminOnly, PropietarioSoloLectura

service = LugaresTuristicosService()


class LugaresTuristicosViewSet(viewsets.ViewSet):
    """
    Equivalente al LugaresTuristicosController de NestJS.
    Propietarios tienen SOLO LECTURA de sus lugares.
    """

    def get_permissions(self):
        # Definir permisos por acción
        action = getattr(self, 'action', None)
        if action == 'create':
            perms = [permissions.IsAuthenticated, IsAdminOnly]  # Solo admin puede crear
        elif action in ('partial_update', 'destroy'):
            perms = [permissions.IsAuthenticated, IsAdminOnly]  # Solo admin puede editar/borrar
        elif action in ('list', 'retrieve'):
            perms = [PropietarioSoloLectura]  # Propietarios ven solo sus lugares
        else:
            perms = [permissions.AllowAny]
        return [p() for p in perms]

    def get_serializer_class(self):
        """Usa el serializer básico para simplicidad."""
        return LugaresTuristicoSerializer

    def list(self, request):
        # FILTRAR AUTOMÁTICAMENTE PARA PROPIETARIOS
        lugares = service.find_all()
        
        # Si es propietario: solo mostrar SUS lugares
        if hasattr(request.user, 'propietario'):
            lugares = [l for l in lugares if getattr(l, 'propietario', None) == request.user]
        
        # Query parameter para vista específica (?view=tourist/owner/simple)
        view_type = request.GET.get('view', 'auto')
        
        if view_type == 'tourist':
            # Vista simplificada para turistas: solo lugares activos
            lugares = [l for l in lugares if getattr(l, 'activo', True)]
            serializer = LugaresTuristicoSerializer(lugares, many=True)
            return Response({
                'lugares': serializer.data,
                'vista': 'turista',
                'mensaje': 'Lugares disponibles para visitar'
            })
        elif view_type == 'owner' and hasattr(request.user, 'propietario'):
            # Vista para propietarios: sus lugares (ya filtrados arriba)
            serializer = LugaresTuristicoSerializer(lugares, many=True)
            return Response({
                'mis_lugares': serializer.data,
                'vista': 'propietario',
                'total': len(serializer.data),
                'solo_lectura': True  # Indicar que es solo lectura
            })
        elif view_type == 'simple':
            # Vista ultra-simple: solo nombre y ubicación
            simple_data = [{'nombre': l.nombre_lugar, 'ubicacion': l.ubicacion} for l in lugares]
            return Response({'lugares': simple_data, 'vista': 'simple'})
        
        # Vista completa (default)
        serializer = LugaresTuristicoSerializer(lugares, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        lugar = service.find_one(pk)
        serializer = LugaresTuristicoSerializer(lugar, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        fotos = request.FILES.getlist('fotos') if 'fotos' in request.FILES else []
        # Usar serializer base para creación (validación)
        serializer = LugaresTuristicoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data['fotos'] = fotos
        lugar = service.create(data)
        
        # Responder con el lugar creado
        response_serializer = LugaresTuristicoSerializer(lugar, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        lugar = service.update(pk, request.data)
        serializer = LugaresTuristicoSerializer(lugar, context={'request': request})
        return Response(serializer.data)

    def destroy(self, _request, pk=None):
        service.remove(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
