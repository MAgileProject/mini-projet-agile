from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import LoginForm, RegisterForm, ProfileForm




# ---------------- LOGIN ----------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
                return render(request, "accounts/login.html", {"form": form})

            if not user.check_password(password):
                messages.error(request, "Invalid email or password.")
                return render(request, "accounts/login.html", {"form": form})

            if not user.is_active:
                messages.error(request, "Your account is disabled.")
                return render(request, "accounts/login.html", {"form": form})

            # Save session
            request.session["user_id"] = user.id
            request.session["is_admin"] = user.is_admin

            #Redirection selon rôle
            if user.is_admin:
                return redirect("admin_dashboard")
            else:
                return redirect("home")

    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


# ---------------- LOGOUT ----------------
def logout_view(request):
    request.session.flush()
    return redirect("login")
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            raw_password = form.cleaned_data["password"]
            user.set_password(raw_password)

            user.is_admin = False
            user.is_active = True

            user.save()

            messages.success(request, "Account created! You can now login.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def index(request):
    return render(request, "accounts/index.html")


# ---------------- USER HOME ----------------
def home(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.is_admin:
        return redirect("admin_dashboard")

    return render(request, "accounts/home.html", {"user": user, "user_name": user.firstname})



# ---------------- PROFILE ----------------
def profile(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    return render(request, "accounts/profile.html", {"form": form, "user": user})



# ---------------- DELETE ACCOUNT ----------------
def delete_account(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    user.delete()

    request.session.flush()
    return redirect("login")



# ---------------- ADMIN DASHBOARD ----------------
def admin_dashboard(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    admin = User.objects.get(id=user_id)

    if not admin.is_admin:
        return redirect("home")

    users = User.objects.filter(is_admin=False)

    return render(request, "accounts/admin_dashboard.html", {"admin": admin, "users": users})



# ---------------- ADMIN EDIT USER ----------------
from django.shortcuts import render, redirect, get_object_or_404

def admin_edit_user(request, user_id):
    if not request.session.get("is_admin"):
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully.")
            return redirect("admin_dashboard")
    else:
        form = ProfileForm(instance=user)

    return render(request, "accounts/admin_edit_user.html", {"form": form, "user": user})

def admin_delete_user(request, user_id):
    if not request.session.get("is_admin"):
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    # L’admin ne peut PAS s’auto-supprimer
    if user.id == request.session.get("user_id"):
        messages.error(request, "You cannot delete your own admin account.")
        return redirect("admin_dashboard")

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("admin_dashboard")



# ---------------- ADMIN TOGGLE USER STATUS ----------------
def toggle_user_status(request, user_id):
    admin_id = request.session.get("user_id")

    if not admin_id:
        return redirect("login")

    admin = User.objects.get(id=admin_id)

    if not admin.is_admin:
        return redirect("home")

    target = User.objects.get(id=user_id)
    target.is_active = not target.is_active
    target.save()

    return redirect("admin_dashboard")
