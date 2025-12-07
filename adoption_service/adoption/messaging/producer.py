from .connection import get_connection
import json

def publish_adoption(data):
    connection, channel = get_connection()
    queue = "adoption_queue"   # même nom que le consumer

    channel.queue_declare(queue=queue, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(data)
    )

    print("[✔] Message envoyé à adoption_queue :", data)

    connection.close()
