# API REST - Proyecto 5to (Django)

Este repositorio contiene una API REST desarrollada con Django y Django REST Framework para una aplicación de guía turística/reservas/reseñas. El proyecto organiza recursos en varias apps: `usuarios`, `servicios`, `resena` y `guia_cultural`. A continuación se documenta la funcionalidad principal, requisitos, cómo levantar el proyecto y los endpoints públicos registrados.

## Resumen 

- Stack: Python, Django, Django REST Framework
- Archivos clave: `manage.py`, `core/settings.py`, apps: `usuarios`, `servicios`, `resena`, `guia_cultural`.
- Base de datos: Postgres (`dd.postgres` en repositorio de desarrollo)
- Media: carpeta `media/` con subcarpetas `lugares/` y `resenas/` para archivos subidos.

## Requisitos

- Python 3.10+ (usar la versión definida en tu entorno local)
- pip
- Virtualenv (recomendado)
Instalación de dependencias (desde la raíz del proyecto):

```powershell
````gcc-md
# API REST - Proyecto 5to

Esta API forma el backend del Proyecto 5to, una aplicación pensada para gestionar información turística de forma práctica y clara. Si preferís una explicación corta: permite manejar usuarios, servicios turísticos, reseñas con fotos y contenidos de guía cultural.

Qué hace, en pocas palabras
- Gestiona distintos tipos de usuario (por ejemplo administrador, propietario, turista).
- Permite publicar y consultar servicios turísticos: atracciones, hoteles, restaurantes, transporte y visitas.
- Soporta reseñas de servicios y subir fotos asociadas a reseñas o lugares.
- Contiene secciones de guía cultural con información y recursos para los usuarios.

Áreas principales
- Usuarios: control de cuentas y roles.
- Servicios: CRUD de lugares y servicios turísticos.
- Reseñas: comentarios y fotos de usuarios sobre servicios.
- Guía cultural: contenidos informativos y recursos.

Sobre imágenes y archivos
Las fotos que suben los usuarios se guardan en el directorio `media/` (organizadas por tipo). En desarrollo Django puede servirlas directamente; en producción conviene usar un sistema de archivos o almacenamiento externo.

Notas rápidas
- La API está organizada en aplicaciones que facilitan extenderla o mantenerla.
> Nota: los includes principales se configuran en `core/urls.py` (por ejemplo `path('servicios/', include('servicios.urls'))`). La app `guia_cultural` contiene su router propio en `guia_cultural/urls.py`.

## Autenticación y permisos (visión)

La API distingue roles de usuario (administrador, propietario, turista, etc.) y aplica permisos por ViewSet. La configuración de autenticación y permisos está centralizada en `core/settings.py` y en los módulos de la app `usuarios`. Los endpoints pueden estar protegidos y, por tanto, pueden requerir autenticación para operaciones de escritura.


## Resumen final
Este proyecto proporciona una API REST modular para una plataforma turística: gestión de usuarios por roles, recursos de servicios turísticos, reseñas con soporte para imágenes y contenidos de guía cultural. La estructura en apps facilita mantenimiento y extensibilidad, y los ViewSets con `DefaultRouter` ofrecen una interfaz RESTful consistente para clientes.

````

Cada ViewSet expone los verbos REST para manejar recursos turísticos, fotos asociadas, y visitas.

3) Reseñas (prefijo: `/resena/`)
- /resena/resena/ → `ResenaViewSet`
- /resena/fotos-resena/ → `FotoResenaViewSet`

Permiten crear y listar reseñas de servicios y añadir/obtener fotos de reseñas. El almacenamiento de imágenes se coloca bajo `media/resenas/`.

4) Guia Cultural (router en `guia_cultural/urls.py`)
- /guia-cultural/ → `GuiaCulturalViewSet` (basename: guia-cultural)

Nota: como se indicó, `guia_cultural.urls` existe y registra `guia-cultural` en su router; si no lo ves en la raíz, añade el include en `core/urls.py` con el prefijo que prefieras.

## Ejemplos de uso (curl / HTTPie)
Listar lugares turísticos (GET):

```powershell
curl http://127.0.0.1:8000/servicios/lugares-turisticos/
```

Crear una reseña (POST) — ejemplo con JSON:

```powershell
curl -X POST http://127.0.0.1:8000/resena/resena/ -H "Content-Type: application/json" -d "{\"titulo\": \"Muy bueno\", \"contenido\": \"Me gustó\", \"servicio\": 1, \"autor\": 2}"
```

Subir una foto para una reseña (multipart/form-data):

```powershell
curl -X POST http://127.0.0.1:8000/resena/fotos-resena/ -F "resena=1" -F "imagen=@C:\ruta\a\foto.jpg"
```


## Autenticación y permisos
- El proyecto incluye la app `usuarios` con roles distintos (administrador, propietario, turista, usuario). Revisa `usuarios/permissions.py` y `usuarios/views/` para la lógica de permisos.

## Media y archivos estáticos
- `MEDIA_URL` y `MEDIA_ROOT` están configurados y, cuando `DEBUG=True`, `core/urls.py` sirve archivos media automáticamente. Revisa `media/lugares/` y `media/resenas/` para fotos subidas.

## Estructura del proyecto (resumen)

- `core/` — configuración del proyecto (settings, urls, wsgi/asgi)
- `usuarios/` — modelos de usuario y ViewSets para los distintos roles
- `servicios/` — modelos/serializers/views para atracciones, hoteles, restaurantes, fotos, visitas
- `resena/` — reseñas y fotos de reseñas (submódulos `models`, `serializers`, `services`, `views`)
- `guia_cultural/` — ViewSet para contenidos de guía cultural




