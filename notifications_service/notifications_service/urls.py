from django.shortcuts import redirect
from django.urls import path, include

def home_redirect(request):
    return redirect("/notifications/")

urlpatterns = [
    path("", home_redirect),  # redirect root to notifications
    path("notifications/", include("notifications.urls")),
    
]
