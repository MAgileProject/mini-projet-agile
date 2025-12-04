import requests

def get_service_url(service_name):
    try:
        data = requests.get("http://127.0.0.1:8500/v1/catalog/service/" + service_name).json()
        if len(data) == 0:
            return None

        service = data[0]
        address = service["ServiceAddress"]
        port = service["ServicePort"]

        return f"http://{address}:{port}"
    except:
        return None
