from django.apps import AppConfig

class IFPSystemAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IFPSystem'

    def ready(self):
        import IFPSystem.signals