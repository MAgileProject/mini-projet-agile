import json

from notifications.models import Notification
from .connection import get_connection


def callback(ch, method, properties, body):
    """Callback RabbitMQ pour traiter les événements d’adoption."""

    data = json.loads(body)
    print("[Consumer] Received:", data)

    # Vérifier que le message contient les informations nécessaires
    if "user_id" not in data or "animal_id" not in data:
        print("⚠ Ignoring message (invalid format)")
        return

    # Construire le message à afficher
    msg = ""
    if data["event"] == "adoption_approved":
        msg = (
            f"Votre demande d'adoption de l'animal "
            f"{data['animal_name']} a été ACCEPTÉE 🎉"
        )
    elif data["event"] == "adoption_rejected":
        msg = (
            f"Votre demande d'adoption de l'animal "
            f"{data['animal_name']} a été REFUSÉE ❌"
        )
    else:
        msg = f"Notification reçue : {data}"

    # Sauvegarder la notification en base
    Notification.objects.create(
        user_id=data["user_id"],
        animal_id=data["animal_id"],
        message=msg,
    )

    print("📩 Notification saved in database.")


def start_consumer():
    """Démarre le consumer RabbitMQ pour le service notifications."""

    print("[INFO] Starting notifications RabbitMQ consumer...")

    connection, channel = get_connection()

    channel.queue_declare(
        queue="adoption_queue",
        durable=True,
    )

    channel.basic_consume(
        queue="adoption_queue",
        on_message_callback=callback,
        auto_ack=True,
    )

    print("[Consumer] Waiting for messages...")
    channel.start_consuming()
