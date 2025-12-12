import requests

CONSUL_URL = "http://127.0.0.1:8500"


def get_service_url(service_name: str) -> str | None:
    """
    Resolve a service URL from Consul.
    Works without Docker (local development).

    Example:
        get_service_url("adoption-service")
        → http://127.0.0.1:8003
    """
    try:
        response = requests.get(
            f"{CONSUL_URL}/v1/catalog/service/{service_name}",
            timeout=2
        )
        response.raise_for_status()

        services = response.json()
        if not services:
            return None

        service = services[0]

        address = service.get("ServiceAddress") or service.get("Address")
        port = service.get("ServicePort")

        if not address or not port:
            return None

        return f"http://{address}:{port}"

    except requests.RequestException as e:
        print(f"[CONSUL] Cannot resolve {service_name}: {e}")
        return None
