import pika
import json

def send_animal_event(event_type, data):
    """Send animal event to RabbitMQ"""
    try:
        # Parse RabbitMQ URL
        url = os.getenv('RABBITMQ_URL', settings.RABBITMQ_URL)
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        # Declare exchange
        channel.exchange_declare(
            exchange='animal_events',
            exchange_type='topic',
            durable=True
        )
        
        # Publish message
        message = {
            'event_type': event_type,
            'data': data,
            'service': 'animals-service'
        }
        
        channel.basic_publish(
            exchange='animal_events',
            routing_key=event_type,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        
        connection.close()
        return True
    except Exception as e:
        print(f"Error sending RabbitMQ message: {e}")
        return False