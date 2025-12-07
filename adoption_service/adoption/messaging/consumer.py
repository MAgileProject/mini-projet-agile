import json
from .connection import get_connection

QUEUE_NAME = "adoption_queue"

def callback(ch, method, properties, body):
    message = json.loads(body)
    print("[ADOPTION] 📥 message reçu :", message)

def start_consumer():
    _, channel = get_connection()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    print("[ADOPTION] 🎧 En attente de messages...")

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
        auto_ack=True
    )

    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
