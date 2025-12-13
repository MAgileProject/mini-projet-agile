from django.shortcuts import render, redirect
import requests

from .models import Notification


def get_user_id_from_accounts(request):
    """
    Calls accounts_service to know who is logged in.
    Uses cookies to forward session.
    """
    try:
        r = requests.get(
            "http://127.0.0.1:8001/api/me/",
            cookies=request.COOKIES,
            timeout=3
        )
        if r.status_code != 200:
            return None
        return r.json().get("id")
    except Exception as e:
        print("ERROR calling accounts_service /api/me/:", e)
        return None


def my_notifications(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("http://127.0.0.1:8001/login/")

    return redirect("user_notifications", user_id=user_id)


def user_notifications(request):
    """
    Show notifications for the currently logged-in user
    (user_id stored in session by accounts_service)
    """
    user_id = request.session.get("user_id")

    

    notifications = Notification.objects.filter(
        user_id=user_id
    ).order_by("-created_at")

    return render(request, "notifications/user_notifications.html", {"notifications": notifications})
