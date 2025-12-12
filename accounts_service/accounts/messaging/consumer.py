import json
from .connection import get_connection

QUEUE_NAME = "notifications"

def callback(ch, method, properties, body):
    msg = json.loads(body.decode("utf-8"))
    event = msg.get("event_type")
    payload = msg.get("payload")

    print("📥 [ACCOUNTS] Notification reçue :", event, payload)

    # Tu peux implémenter ton traitement ici
    if event == "ADOPTION_ACCEPTED":
        print("→ Informer l’utilisateur que son adoption est acceptée")

    if event == "ADOPTION_REFUSED":
        print("→ Informer que l’adoption est refusée")

    if event == "APPOINTMENT_CONFIRMED":
        print("→ Informer que le rendez-vous est confirmé")

    # etc.


def start_consumer():
    connection, channel = get_connection()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("[ACCOUNTS] 🎧 En attente de notifications...")

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True,
    )

    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
