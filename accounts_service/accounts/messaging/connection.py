import pika
from django.conf import settings

def get_connection():
    """
    Création de la connexion + channel RabbitMQ via settings.RABBITMQ_URL.
    """
    params = pika.URLParameters(settings.RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    return connection, channel
