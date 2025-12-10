import requests
from django.http import JsonResponse
from .models import AdoptionRequest
from adoption_service.utils import get_service_url
from django.shortcuts import render
from django.http import HttpResponse
from adoption.messaging.producer import publish_adoption
from django.shortcuts import redirect

from adoption_service.utils import get_service_url
import requests
def home(request):
    return HttpResponse("<h1>Bienvenue dans Adoption-Service</h1>")
def home(request):
    return render(request, "home.html")
# ▶️ 1. Créer une demande d’adoption


def create_request(request):
    if request.method == "GET":
        return render(request, "form_adoption.html")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        animal_id = request.POST.get("animal_id")
        appointment_id = request.POST.get("appointment_id")

        if not user_id or not animal_id:
            return render(request, "form_adoption.html", {
                "error": "User ID et Animal ID sont obligatoires."
            })

        req = AdoptionRequest.objects.create(
            user_id=int(user_id),
            animal_id=int(animal_id),
            appointment_id=int(appointment_id) if appointment_id else None,
            status="pending"
        )

        return render(request, "success_adoption.html", {
            "request": req
        })


def user_requests(request, user_id):
    reqs = AdoptionRequest.objects.filter(user_id=user_id).order_by("-date_requested")
    return render(request, "liste_adoptions.html", {"reqs": reqs})


# ▶️ 2. Voir le statut
def request_status(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)
        return JsonResponse({
            "id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id,
            "status": req.status,
            "date": req.date_requested
        })
    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)




def reject_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        req.status = "rejected"
        req.save()

        # 📩 envoyer un message RabbitMQ
        publish_adoption({
            "event": "adoption_rejected",
            "request_id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id
        })

        return JsonResponse({"success": True})

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Demande introuvable"}, status=404)

def cancel_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        if req.status != "pending":
            return JsonResponse({"error": "Impossible d'annuler une demande déjà traitée"}, status=400)

        req.status = "cancelled"
        req.save()
        return JsonResponse({"success": True, "message": "Demande annulée"})
    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Demande introuvable"}, status=404)

def admin_list(request):
    reqs = AdoptionRequest.objects.all().order_by("-date_requested")
    return render(request, "admin_list.html", {"reqs": reqs})

def approve_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        req.status = "approved"
        req.save()

        # 📩 Envoyer un message RabbitMQ
        publish_adoption({
            "event": "adoption_approved",
            "user_id": req.user_id,
            "animal_id": req.animal_id,
            "request_id": req.id
        })

        return redirect("/adoption/admin/requests/")

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Demande introuvable"}, status=404)
    
def reject_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        req.status = "rejected"
        req.save()

        # Notifier le client
        send_notification("notifications", {
            "type": "adoption_rejected",
            "user_id": req.user_id,
            "animal_id": req.animal_id
        })

        return JsonResponse({"success": True})

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Demande introuvable"}, status=404)      