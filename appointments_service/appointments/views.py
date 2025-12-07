from django.shortcuts import render
from django.shortcuts import render, redirect

from appointments_service import appointments
from .models import RendezVous
from appointments_service.utils import get_service_url
import requests

def prendre_rdv(request):
    animals_url = get_service_url("animals-service")
    animals = []

    if animals_url:
        try:
            animals = requests.get(animals_url + "api/animals/").json()
        except requests.RequestException:
            animals = []

    if request.method == "POST":
        user = request.POST["user"]
        animal = request.POST["animal"]
        date = request.POST["date"]

        RendezVous.objects.create(
            user_id=user,
            animal_id=animal,
            date=date,
        )
        return redirect("liste_rdv")

    return render(request, "prendre_rdv.html", {"animals": animals})
