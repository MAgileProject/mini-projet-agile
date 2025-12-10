from django.apps import AppConfig
from django.conf import settings
import threading
import requests

class AnimalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'animals'

    def ready(self):
        # Register service in Consul in a background thread
        def register():
            try:
                payload = {
                    "Name": settings.SERVICE_NAME,
                    "ID": settings.SERVICE_ID,
                    "Port": settings.SERVICE_PORT,
                    "Tags": ["animals", "django", "microservice"],
                    "Check": {
                        "HTTP": f"http://{settings.SERVICE_NAME}:{settings.SERVICE_PORT}/health/",
                        "Interval": "10s"
                    }
                }
                url = f"http://{settings.CONSUL_HOST}:{settings.CONSUL_PORT}/v1/agent/service/register"
                requests.put(url, json=payload, timeout=3)
            except Exception:
                # Do not break Django if Consul is not reachable
                pass

        threading.Thread(target=register, daemon=True).start()
