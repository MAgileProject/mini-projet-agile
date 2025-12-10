from email.policy import default
from django.apps import AppConfig


class AdoptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoption'
    
    def ready(self):
        try:
            from . import consumers  # noqa
        except Exception:
            pass