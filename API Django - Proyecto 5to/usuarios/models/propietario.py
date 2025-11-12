from django.db import models
from django.apps import apps
from django.utils import timezone
from usuarios.models.usuario import Usuario

class Propietario(Usuario):
    tipo_negocio = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'propietarios'
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'


    def ver_negocio(self):
        """
        Devuelve información resumida del/los servicios que pertenecen a este
        propietario y las marcas de visita ('VisitIntent') que los turistas
        han creado con estado 'ira'.

        Resultado: diccionario con keys 'services' y 'visit_marks'.
        """
        Servicio = apps.get_model('servicios', 'Servicio')
        Visita = apps.get_model('servicios', 'Visita')

        servicios = Servicio.objects.filter(propietario=self)

        services_list = [
            {
                'id': str(s.pk),
                'tipo_servicio': s.tipo_servicio,
                'descripcion': s.descripcion,
                'horario': s.horario,
            }
            for s in servicios
        ]

        # Obtener marcas de visita confirmadas (estado 'ira') ordenadas por fecha_visita o creación
        now = timezone.now()
        visita_qs = Visita.objects.filter(
            servicio__in=servicios,
            estado='ira'
        ).select_related('usuario', 'servicio').order_by('fecha_visita', '-created_at')

        visita_marks = []
        for v in visita_qs:
            # opcional: sólo considerar marcas futuras si fecha_visita indicada
            if v.fecha_visita and v.fecha_visita < now:
                # si la fecha ya pasó, ignore (o podríamos mostrarlo como histórico)
                continue
            visita_marks.append({
                'mark_id': str(v.pk),
                'usuario_id': str(v.usuario.pk),
                'usuario_nombre': getattr(v.usuario, 'nombre', str(v.usuario)),
                'servicio_id': str(v.servicio.pk),
                'servicio_tipo': v.servicio.tipo_servicio,
                'fecha_visita': v.fecha_visita,
                'estado': v.estado,
                'nota': v.nota,
                'created_at': v.created_at,
            })

        return {
            'services': services_list,
            'visit_marks': visita_marks,
        }