from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from django.shortcuts import render
from .serializers import NotificationSerializer
from django.shortcuts import render
from .models import Notification
from django.shortcuts import render

def notifications_home(request):
    return render(request, "notifications/home.html")

class NotificationViewSet(viewsets.ModelViewSet):
    """
    /notifications/api/notifications/
    /notifications/api/notifications/<id>/
    """
    queryset = Notification.objects.all().order_by("-created_at")
    serializer_class = NotificationSerializer

    @action(detail=False, methods=["get"])
    def my(self, request):
        """
        /notifications/api/notifications/my/
        Retourne les notifs du user courant (X-User-ID)
        """
        user_id = request.headers.get("X-User-ID")
        if not user_id:
            return Response(
                {"detail": "Missing X-User-ID header"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = Notification.objects.filter(user_id=user_id).order_by("-created_at")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def mark_read(self, request, pk=None):
        """
        /notifications/api/notifications/<id>/mark_read/
        """
        notif = self.get_object()
        notif.read = True
        notif.save()
        return Response({"status": "ok"})


def my_notifications_html(request):
    """
    Vue HTML pour afficher les notifs d'un user.
    Utilise X-User-ID (fourni par accounts_service / gateway).
    """
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        return render(request, "notifications/error.html", {
            "message": "Missing X-User-ID header.",
        })

    notifications = Notification.objects.filter(user_id=user_id).order_by("-created_at")

    return render(request, "notifications/list.html", {
        "notifications": notifications,
    })

def api_notifications(request):
    """
    Return all notifications in JSON format (for testing).
    """
    data = list(Notification.objects.values())
    return JsonResponse(data, safe=False)


def my_notifications(request):
    return render(request, "notifications/my_notifications.html")

def user_notifications(request, user_id):
     # type: ignore # accounts-service

    notifications = Notification.objects.filter(user_id=user_id).order_by("-created_at")
    return render(request, "notifications/user_notifications.html", {"notifications": notifications})
