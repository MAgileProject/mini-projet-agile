from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from animals_service.utils import get_service_url

from .models import Animal
from .forms import AnimalForm
from .serializers import AnimalSerializer


# ============================
# ROLE CHECK (DEV MODE + header)
# ============================

def is_admin(request):
    # DEV MODE: force admin view while developing
    if getattr(settings, "DEV_MODE", False):
        return True

    role = request.headers.get("X-User-Role", "user")
    return role.lower() == "admin"


# ============================
# FILTER SYSTEM
# ============================

def filter_animals(request):
    qs = Animal.objects.all().order_by("-created_at")

    q = request.GET.get("q")
    species = request.GET.get("type")
    breed = request.GET.get("breed")
    age = request.GET.get("age")
    location = request.GET.get("location")
    vaccinated = request.GET.get("vaccinated")

    if q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(breed__icontains=q)
        )
    if species:
        qs = qs.filter(type__icontains=species)
    if breed:
        qs = qs.filter(breed__icontains=breed)
    if age:
        qs = qs.filter(age__icontains=age)
    if location:
        qs = qs.filter(location__icontains=location)
    if vaccinated == "true":
        qs = qs.filter(vaccinated=True)

    return qs


# ============================
# CLIENT VIEWS
# ============================

def catalog_view(request):
    animals = filter_animals(request).filter(status="available")

    adoption_url = get_service_url("adoption-service")

    return render(request, "animals/catalog.html", {
        "animals": animals,
        "adoption_url": adoption_url,
        "user_id": request.session.get("user_id"),
    })

def animal_detail(request, pk):
    if is_admin(request):
        return redirect("admin_dashboard")

    animal = get_object_or_404(Animal, pk=pk)
    return render(request, "animals/detail.html", {"animal": animal})


def client_propose_animal(request):
    if is_admin(request):
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.status = "pending"
            a.submitted_by_user = True
            a.save()
            messages.success(request, "Your animal proposal has been submitted!")
            return redirect("catalog")
    else:
        form = AnimalForm()

    return render(request, "animals/propose.html", {"form": form})


# ============================
# ADMIN VIEWS
# ============================

def admin_dashboard(request):
    if not is_admin(request):
        return redirect("catalog")

    stats = {
        "total_animals": Animal.objects.count(),
        "pending_animals": Animal.objects.filter(status="pending").count(),
        "available_animals": Animal.objects.filter(status="available").count(),
        "reserved_animals": Animal.objects.filter(status="reserved").count(),
        "adopted_animals": Animal.objects.filter(status="adopted").count(),
    }

    return render(request, "animals/admin_dashboard.html", stats)


def admin_manage_animals(request):
    if not is_admin(request):
        return redirect("catalog")

    animals = Animal.objects.all()
    return render(request, "animals/admin_manage.html", {"animals": animals})


def admin_pending(request):
    if not is_admin(request):
        return redirect("catalog")

    animals = Animal.objects.filter(status="pending")
    return render(request, "animals/admin_pending.html", {"animals": animals})


# ============================
# PUBLIC API
# ============================

class AnimalListCreateAPI(generics.ListCreateAPIView):
    serializer_class = AnimalSerializer

    def get_queryset(self):
        return filter_animals(self.request)


class AnimalRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


@api_view(["POST"])
def request_adoption_api(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if animal.status != "available":
        return Response({"error": "Animal not available"}, status=400)

    animal.status = "reserved"
    animal.save()

    return Response({"message": "Adoption request sent!"})


# ============================
# ADMIN API ACTIONS
# ============================

@api_view(["POST"])
def approve_animal_api(request, pk):
    if not is_admin(request):
        return Response({"error": "Unauthorized"}, status=403)

    animal = get_object_or_404(Animal, pk=pk)
    animal.status = "available"
    animal.submitted_by_user = False
    animal.save()
    return redirect("admin_pending")


@api_view(["POST"])
def reject_animal_api(request, pk):
    if not is_admin(request):
        return Response({"error": "Unauthorized"}, status=403)

    animal = get_object_or_404(Animal, pk=pk)
    animal.delete()
    return redirect("admin_pending")

def admin_delete_animal(request, pk):
    animal = get_object_or_404(Animal, id=pk)
    animal.delete()
    return redirect('admin_manage_animals')


def admin_edit_animal(request, pk):
    animal = get_object_or_404(Animal, id=pk)

    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('admin_manage_animals')
    else:
        form = AnimalForm(instance=animal)

    return render(request, "animals/admin_edit.html", {"form": form, "animal": animal})


def admin_reserved_animals(request):
    if not is_admin(request):
        return redirect("catalog")

    animals = Animal.objects.filter(status="reserved")
    return render(request, "animals/admin_reserved.html", {"animals": animals})


def admin_adopted_animals(request):
    if not is_admin(request):
        return redirect("catalog")

    animals = Animal.objects.filter(status="adopted")
    return render(request, "animals/admin_adopted.html", {"animals": animals})


