from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class PolicyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'policyapp'

    def ready(self):
        from .schedulers import start_scheduler  # Import inside ready() to avoid issues
        start_scheduler()
        logger.info("🔌 Scheduler triggered from AppConfig ready()")
