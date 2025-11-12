from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db import transaction
from servicios.models.visita import Visita
from servicios.serializers.visita_serializer import VisitaSerializer
from usuarios.permissions import  VisitasSoloLecturaPropietario


class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all() #pylint: disable=no-member
    serializer_class = VisitaSerializer

    def get_permissions(self):
        """
        Permisos por acción:
        - CREATE: Solo usuarios autenticados (turistas) pueden marcar visitas
        - LIST/RETRIEVE: Propietarios ven sus visitas (solo lectura), usuarios ven las suyas
        - UPDATE/DELETE: Solo usuarios pueden editar sus propias visitas (propietarios NO)
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('list', 'retrieve'):
            permission_classes = [permissions.IsAuthenticated]
        else:  # update, partial_update, destroy
            permission_classes = [permissions.IsAuthenticated, VisitasSoloLecturaPropietario] 
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'propietario'):
            return Visita.objects.filter(servicio__propietario=user) #pylint: disable=no-member
        return Visita.objects.filter(usuario=user) #pylint: disable=no-member
    
    def list(self, request, *args, **kwargs):
        """Override list para indicar modo solo lectura a propietarios."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Si es propietario, agregar metadata de solo lectura
        if hasattr(request.user, 'propietario'):
            return Response({
                'visitas_a_mis_lugares': serializer.data,
                'total': len(serializer.data),
                'solo_lectura': True,
                'mensaje': 'Como propietario, puedes ver las visitas pero no editarlas'
            })
        
        # Para turistas/usuarios normales
        return Response(serializer.data)

    def perform_create(self, serializer):
        visita = serializer.save(usuario=self.request.user)

        datos_notificacion = {
            "propietario_id": visita.servicio.propietario.id,
            "servicio_id": visita.servicio.id,
            "usuario_id": visita.usuario.id,
            "estado": visita.estado,
        }

        transaction.on_commit(lambda: self.enviar_notificacion(datos_notificacion))

        return visita

    def perform_update(self, serializer):
        visita = serializer.save()

        datos_notificacion = {
            "propietario_id": visita.servicio.propietario.id,
            "servicio_id": visita.servicio.id,
            "usuario_id": visita.usuario.id,
            "estado": visita.estado,
        }

        transaction.on_commit(lambda: self.enviar_notificacion(datos_notificacion))

        return visita

    # 🔗 Aquí se conecta tu WebSocket en Ruby
    def enviar_notificacion(self, payload):
        """
        aplicar logica de ruby websocket aqui
        """
        # implementar cuando tengas la URL del gateway Ruby
