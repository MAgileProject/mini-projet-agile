from .connection import get_connection
import json

def publish_appointment(data):
    connection, channel = get_connection()
    queue = "appointment_queue"

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data)
    )

    print("[✔] Appointment envoyé :", data)

    connection.close()
