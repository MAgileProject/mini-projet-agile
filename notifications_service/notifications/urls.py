from django.urls import path
from . import views

urlpatterns = [
    path("my/", views.my_notifications, name="my_notifications"),
        path("user/", views.user_notifications, name="user_notifications"),

]
