from .connection import get_connection
import json

def publish_user_created(data):
    connection, channel = get_connection()

    queue = "user_created"

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data)
    )

    print("[✔] Message envoyé :", data)

    connection.close()
