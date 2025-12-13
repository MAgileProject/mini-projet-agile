import requests

def get_current_user_id(request):
    try:
        cookies = request.COOKIES  # on forward le cookie de session
        response = requests.get(
            "http://127.0.0.1:8001/api/me/",
            cookies=cookies,
            timeout=3
        )

        if response.status_code != 200:
            return None

        return response.json().get("id")

    except Exception as e:
        print("Error fetching user from accounts_service:", e)
        return None
