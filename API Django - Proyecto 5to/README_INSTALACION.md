# 🚀 API Django

## 📋 Instrucciones de Instalación

### 🔹 Paso 1: Configurar el proyecto
2. **Abrir terminal** en la carpeta del proyecto
3. **Crear entorno virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

### 🔹 Paso 2: Instalar dependencias
```bash
pip install django djangorestframework psycopg2-binary django-cors-headers channels
```

### 🔹 Paso 3: Instalar y configurar PostgreSQL
1. **Descargar e instalar PostgreSQL** desde: https://www.postgresql.org/download/
2. **Instalar pgAdmin4** (viene incluido)
3. **Crear base de datos:**
   - Abrir pgAdmin4
   - Conectar al servidor PostgreSQL
   - Clic derecho en "Databases" → "Create" → "Database"
   - Nombre: `AppTurismo`
4. **Anotar tu configuración** (usuario, contraseña, puerto)

### 🔹 Paso 4: Configurar settings.py
En `core/settings.py`, actualizar la configuración de PostgreSQL con TUS datos:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'AppTurismo',
        'USER': 'tu_usuario_postgres',      # Cambiar
        'PASSWORD': 'tu_contraseña',        # Cambiar  
        'HOST': 'localhost',
        'PORT': 'tu_puerto',                # Cambiar (normalmente 5432)
    }
}
```

### 🔹 Paso 5: Aplicar migraciones
```bash
python manage.py migrate
```

### 🔹 Paso 6: Crear superusuario
```bash
python manage.py createsuperuser
```

### 🔹 Paso 7: Ejecutar servidor
```bash
python manage.py runserver
```

## 🌐 URLs importantes para ingresar datos y que se hayan actualizado en Postgres:
- **Usuarios**: http://127.0.0.1:8000/usuario/
- **API**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **Hoteles**: http://127.0.0.1:8000/servicios/hotel/


## 🔑 Características del sistema:
- ✅ Sistema de usuarios por roles (Turista, Propietario, Administrador)
- ✅ CRUD completo para hoteles, restaurantes, lugares turísticos
- ✅ Sistema de reseñas con fotos
- ✅ Base de datos PostgreSQL
- ✅ Permisos granulares por rol
- ✅ API REST completa

## 📞 Soporte:
Si hay problemas, revisar que:
1. **PostgreSQL esté corriendo** (servicios de Windows)
2. **La base de datos `AppTurismo` exista** en pgAdmin4
3. **Las credenciales en settings.py sean correctas**
4. **El entorno virtual esté activado** (.venv)
5. **El puerto PostgreSQL sea correcto** (normalmente 5432, no 5433)

## 🔧 Problemas comunes:
- **Error "No module named 'django'"**: Activar entorno virtual
- **Error conexión BD**: Verificar usuario, contraseña y puerto en settings.py
- **Error psycopg2**: Instalar Microsoft Visual C++ Build Tools

¡Listo para usar! 🎉

