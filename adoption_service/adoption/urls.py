from django.urls import path
from . import views

urlpatterns = [
    # CLIENT
    path("create/", views.create_request),
    path("status/<int:id>/", views.request_status),
    path("list/<int:user_id>/", views.user_requests),
    path("cancel/<int:id>/", views.cancel_request),

    # ADMIN
    path("admin/requests/", views.admin_list, name="admin_requests"),
    path("admin/approve/<int:id>/", views.approve_request, name="approve_adoption"),
    path("admin/reject/<int:id>/", views.reject_request, name="reject_adoption"),

]
