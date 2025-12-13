import requests

def get_current_user_id(request):
    """
    Ask account-service who is the currently logged-in user.
    Uses session cookies (microservice-safe).
    """
    try:
        response = requests.get(
            "http://127.0.0.1:8001/api/me/",
            cookies=request.COOKIES,
            timeout=3
        )

        if response.status_code != 200:
            return None

        data = response.json()
        return data.get("id")

    except Exception as e:
        print("ERROR contacting account-service:", e)
        return None
