from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Animal
from .forms import AnimalForm
from .serializers import AnimalSerializer


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
# CLIENT (USER) VIEWS
# ============================

def catalog_view(request):
    animals = filter_animals(request).filter(status="available")
    return render(request, "animals/catalog.html", {"animals": animals})


@api_view(["POST"])
def mark_animal_adopted(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.status = "adopted"
    animal.save()
    return Response({"message": "Animal marked as adopted"})

def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, "animals/detail.html", {"animal": animal})


def client_propose_animal(request):
    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.status = "pending"
            animal.submitted_by_user = True
            animal.save()
            messages.success(request, "Animal proposal sent for validation.")
            return redirect("catalog")
    else:
        form = AnimalForm()

    return render(request, "animals/propose.html", {"form": form})


# ============================
# ADMIN VIEWS
# ============================

def admin_dashboard(request):
    stats = {
        "total_animals": Animal.objects.count(),
        "pending_animals": Animal.objects.filter(status="pending").count(),
        "adopted_animals": Animal.objects.filter(status="adopted").count(),
    }

    return render(request, "animals/admin_dashboard.html", stats)


def admin_manage_animals(request):
    animals = Animal.objects.all()
    return render(request, "animals/admin_manage.html", {"animals": animals})


def admin_pending(request):
    animals = Animal.objects.filter(status="pending")
    return render(request, "animals/admin_pending.html", {"animals": animals})


def admin_reserved_animals(request):
    animals = Animal.objects.filter(status="reserved")
    return render(request, "animals/admin_reserved.html", {"animals": animals})


def admin_adopted_animals(request):
    animals = Animal.objects.filter(status="adopted")
    return render(request, "animals/admin_adopted.html", {"animals": animals})


def admin_edit_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    if request.method == "POST":
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            return redirect("admin_manage_animals")
    else:
        form = AnimalForm(instance=animal)

    return render(request, "animals/admin_edit.html", {"form": form, "animal": animal})


def admin_delete_animal(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.delete()
    return redirect("admin_manage_animals")


# ============================
# API
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
    return Response({"message": "Adoption request sent"})


@api_view(["POST"])
def approve_animal_api(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    animal.status = "available"
    animal.submitted_by_user = False
    animal.save()
    return redirect("admin_pending")


@api_view(["POST"])
def reject_animal_api(request, pk):
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

def admin_add_animal(request):
    if not is_admin(request):
        return redirect("catalog")

    if request.method == "POST":
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.status = "available"   # ADMIN = auto approved
            animal.submitted_by_user = False
            animal.save()
            return redirect("admin_dashboard")
    else:
        form = AnimalForm()

    return render(request, "animals/admin_dashboard.html", {

    })

