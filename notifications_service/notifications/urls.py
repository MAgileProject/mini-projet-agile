from django.urls import path
from . import views

urlpatterns = [
    path("", views.notifications_home, name="notifications_home"),  # NEW
    path("api/", views.api_notifications, name="api_notifications"),
    path("my/", views.my_notifications, name="my_notifications"),
    path("user/<int:user_id>/", views.user_notifications, name="user_notifications"),



]
