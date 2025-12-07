import json
from .connection import get_connection

QUEUE_NAME = "user_created"

def callback(ch, method, properties, body):
    message = json.loads(body)
    print("📥 Message reçu :", message)

def start_consumer():
    _, channel = get_connection()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("🎧 En attente de messages sur :", QUEUE_NAME)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
