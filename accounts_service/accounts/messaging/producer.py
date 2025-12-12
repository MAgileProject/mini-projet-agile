import json
from django.conf import settings
from .connection import get_connection

QUEUE_NAME = "notifications"

def publish_event(event_type: str, payload: dict):
    """
    Envoi d’un message dans RabbitMQ pour les autres microservices.
    Exemple :
        publish_event("USER_REGISTERED", {"user_id": 5})
    """
    try:
        connection, channel = get_connection()
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        message = {
            "event_type": event_type,
            "payload": payload,
        }

        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(message).encode("utf-8"),
        )
        connection.close()
        print(f"[RABBITMQ] Sent {event_type} -> {payload}")

    except Exception as e:
        print(f"[RABBITMQ] ERROR sending message: {e}")
