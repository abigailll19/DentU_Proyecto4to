from servicios.models.visita import Visita


class VisitaService:
    @staticmethod
    def crear_visita(usuario, servicio=None, lugar=None, fecha_visita=None, estado='ira', nota=None):
        """
        Crea una visita para un turista. Debe recibir al menos `servicio` o `lugar`.
        Devuelve la visita creada y, si corresponde, los datos para notificar al propietario.
        """
        if not servicio and not lugar:
            raise ValueError('Se requiere servicio o lugar para crear una visita')

        visita = Visita.objects.create( #pylint: disable=no-member
            usuario=usuario,
            servicio=servicio,
            lugar=lugar,
            fecha_visita=fecha_visita,
            estado=estado,
            nota=nota
        )

        datos_notificacion = None
        if servicio and getattr(servicio, 'propietario', None):
            datos_notificacion = {
                "propietario_id": servicio.propietario.id,
                "servicio_id": servicio.id,
                "usuario_id": usuario.id,
                "estado": estado,
            }

        return visita, datos_notificacion

    @staticmethod
    def actualizar_visita(visita, estado=None, nota=None, fecha_visita=None):
        """
        Actualiza campos permitidos de una visita y devuelve (visita, datos_notificacion|None).
        """
        if estado:
            visita.estado = estado
        if nota is not None:
            visita.nota = nota
        if fecha_visita:
            visita.fecha_visita = fecha_visita
        visita.save()

        datos_notificacion = None
        propietario = visita.get_propietario()
        if propietario:
            datos_notificacion = {
                "propietario_id": propietario.id,
                "servicio_id": visita.servicio.id,
                "usuario_id": visita.usuario.id,
                "estado": visita.estado,
            }

        return visita, datos_notificacion
