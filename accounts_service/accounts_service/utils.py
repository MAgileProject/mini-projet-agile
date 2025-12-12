import requests

CONSUL_URL = "http://127.0.0.1:8500"

def get_service_url(service_name):
    r = requests.get(f"{CONSUL_URL}/v1/catalog/service/{service_name}")
    services = r.json()

    if not services:
        raise Exception(f"Service {service_name} not found")

    service = services[0]
    return f"http://{service['ServiceAddress']}:{service['ServicePort']}"
