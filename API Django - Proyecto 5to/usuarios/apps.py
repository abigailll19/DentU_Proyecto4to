from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    
    def ready(self):
        """Importar señales cuando la app esté lista"""
        import usuarios.signals
