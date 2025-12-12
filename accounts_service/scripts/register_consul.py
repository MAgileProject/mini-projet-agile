import os
import socket
import json
import time
import requests


def _get_host_address():
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = '127.0.0.1'
    return ip


def register_service(retries=5, delay=2):
    consul_host = os.environ.get('CONSUL_HOST', 'consul')
    consul_port = int(os.environ.get('CONSUL_PORT', '8500'))
    service_name = os.environ.get('SERVICE_NAME', 'accounts_service')
    service_port = int(os.environ.get('SERVICE_PORT', '8000'))
    service_id = f"{service_name}-{service_port}"
    address = _get_host_address()

    url = f'http://{consul_host}:{consul_port}/v1/agent/service/register'
    payload = {
        'ID': service_id,
        'Name': service_name,
        'Address': address,
        'Port': service_port,
        'Tags': ['django', 'accounts'],
        'Check': {
            'HTTP': f'http://{address}:{service_port}/api/users/',
            'Interval': '10s'
        }
    }

    for attempt in range(1, retries + 1):
        try:
            resp = requests.put(url, data=json.dumps(payload), timeout=5)
            if resp.status_code in (200, 201, 204):
                print(f'Registered {service_name} at {address}:{service_port}')
                return True
            else:
                print('Consul returned', resp.status_code, resp.text)
        except Exception as e:
            print('Error contacting Consul:', e)

        time.sleep(delay)

    print('Failed to register with Consul')
    return False


if __name__ == '__main__':
    register_service()
