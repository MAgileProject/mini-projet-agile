from django.urls import path
from .views import (
    login_view, logout_view, home, profile, delete_account,
    admin_dashboard, admin_edit_user, toggle_user_status
)

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("home/", home, name="home"),
    path("profile/", profile, name="profile"),
    path("delete-account/", delete_account, name="delete_account"),

    # Admin
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/edit/<int:user_id>/", admin_edit_user, name="admin_edit_user"),
    path("admin/toggle/<int:user_id>/", toggle_user_status, name="toggle_user_status"),
]
