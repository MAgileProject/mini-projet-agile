import sys
import os
import threading
import logging
from django.apps import AppConfig
from django.conf import settings

# --- Consul Registration Logic ---

logger = logging.getLogger(__name__)
# Use a simple flag to ensure registration happens once
registration_performed = False

def register_consul_service():
    """
    Registers the service with the Consul agent.
    """
    global registration_performed
    if registration_performed:
        return

    # Check if a specific environment variable is set to skip registration 
    # (e.g., for local dev or running management commands)
    if os.environ.get('SKIP_CONSUL_REGISTRATION') == 'True':
        logger.info("Skipping Consul registration as requested by environment variable.")
        registration_performed = True
        return
        
    try:
        import consul
    except ImportError:
        logger.error("python-consul is not installed. Skipping Consul registration.")
        registration_performed = True
        return

    try:
        c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        
        # Check endpoint (e.g., for health checks)
        check = consul.Check.http(
            url=f"http://{os.environ.get('SERVICE_IP', 'localhost')}:{settings.SERVICE_PORT}/api/users/",
            interval='10s',
            timeout='5s'
        )
        
        # Register the service
        c.agent.service.register(
            name=settings.SERVICE_NAME,
            service_id=settings.SERVICE_ID,
            address=os.environ.get('SERVICE_IP', 'localhost'), # Use the IP from the environment or default
            port=settings.SERVICE_PORT,
            tags=['django', 'account', 'v1'],
            check=check
        )
        
        logger.info(f"Successfully registered service '{settings.SERVICE_NAME}' with Consul.")
        registration_performed = True
        
    except Exception as e:
        # Do not block startup if Consul is unavailable; log and move on.
        logger.error(f"Failed to register service with Consul at {settings.CONSUL_HOST}:{settings.CONSUL_PORT}. Error: {e}")
        # Note: If registration fails, the service will not be discoverable.
        # A proper production setup would have a periodic retry mechanism.


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        Runs on Django startup.
        """
        # Only run this logic when running the main server
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            # Run the registration in a separate thread to not block the main startup process
            threading.Thread(target=register_consul_service).start()