from django.urls import path ,include
from . import views
from .views import check_adoption
urlpatterns = [

    # ---------------------------------------------
    # 👤 CLIENT ROUTES
    # ---------------------------------------------
    path("", views.home, name="adoption_home"),
    path("create/", views.create_request, name="create_adoption"),
    path("list/<int:user_id>/", views.user_requests, name="user_adoptions"),
    path("status/<int:id>/", views.request_status, name="request_status"),
    path("cancel/<int:id>/", views.cancel_request, name="cancel_request"),
    path("notifications/<int:user_id>/", views.go_to_notifications, name="go_to_notifications"),

    # ---------------------------------------------
    # 👨‍💼 ADMIN ROUTES
    # ---------------------------------------------
    path("admin/", views.admin_list, name="admin_requests"),
    path("admin/approve/<int:id>/", views.approve_request, name="approve_request"),
    path("admin/reject/<int:id>/", views.reject_request, name="reject_request"),
    path('adoptions/check/<int:user_id>/<int:animal_id>/', check_adoption),
]
