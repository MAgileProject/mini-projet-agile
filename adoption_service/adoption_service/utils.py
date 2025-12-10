import requests

CONSUL = "http://127.0.0.1:8500/v1/catalog/service/"

def get_service_url(service_name):
    try:
        res = requests.get(CONSUL + service_name).json()

        if len(res) == 0:
            return None

        address = res[0]["ServiceAddress"] or "127.0.0.1"
        port = res[0]["ServicePort"]

        return f"http://{address}:{port}/"

    except:
        return None
