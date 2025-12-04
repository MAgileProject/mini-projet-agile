import requests

CONSUL_URL = "http://127.0.0.1:8500/v1/catalog/service/"

def get_service_url(service_name):
    try:
        response = requests.get(CONSUL_URL + service_name)
        data = response.json()

        if len(data) == 0:
            return None

        address = data[0]["ServiceAddress"] or "127.0.0.1"
        port = data[0]["ServicePort"]

        return f"http://{address}:{port}/"
    except:
        return None
