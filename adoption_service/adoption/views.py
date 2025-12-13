import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import AdoptionRequest
from adoption_service.utils import get_service_url
from adoption.messaging.producer import publish_adoption

from adoption_service.utils import get_service_url


def redirect_to_login():
    accounts_url = get_service_url("accounts-service")
    return redirect(f"{accounts_url}/login/")

# -------------------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------------------
def home(request):
    return render(request, "client/home.html")


# -------------------------------------------------------------------
# CREATE ADOPTION REQUEST
# -------------------------------------------------------------------
def create_request(request):
    # GET: open form with prefilled animal_id
    if request.method == "GET":
        animal_id = request.GET.get("animal_id")

        return render(request, "client/form_adoption.html", {
            "animal_id": animal_id
        })

    # POST: submit adoption
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        animal_id = request.POST.get("animal_id")
        appointment_id = request.POST.get("appointment_id")

        if not user_id or not animal_id:
            return render(request, "form_adoption.html", {
                "error": "User ID and Animal ID are required",
                "animal_id": animal_id
            })

        req = AdoptionRequest.objects.create(
            user_id=user_id,
            animal_id=animal_id,
            appointment_id=appointment_id or None,
            status="pending"
        )

        return render(request, "client/success_adoption.html", {"request": req})


# -------------------------------------------------------------------
# LIST USER REQUESTS
# -------------------------------------------------------------------
def user_requests(request, user_id):
    reqs = AdoptionRequest.objects.filter(user_id=user_id).order_by("-date_requested")
    return render(request, "client/liste_adoptions.html", {"reqs": reqs})


# -------------------------------------------------------------------
# REQUEST STATUS (API)
# -------------------------------------------------------------------
def request_status(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)
        return JsonResponse({
            "id": req.id,
            "user_id": req.user_id,
            "animal_id": req.animal_id,
            "status": req.status,
            "date": req.date_requested,
        })
    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)


# -------------------------------------------------------------------
# CANCEL REQUEST
# -------------------------------------------------------------------
def cancel_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        if req.status != "pending":
            return JsonResponse({"error": "Cannot cancel a processed request"}, status=400)

        req.status = "cancelled"
        req.save()
        return JsonResponse({"success": True})

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)


# -------------------------------------------------------------------
# ADMIN LIST
# -------------------------------------------------------------------
def admin_list(request):
    reqs = AdoptionRequest.objects.all().order_by("-date_requested")
    return render(request, "admin/admin_list.html", {"reqs": reqs})


# -------------------------------------------------------------------
# APPROVE REQUEST (FIXED)
# -------------------------------------------------------------------



def approve_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)

        # 1️⃣ Update adoption status
        req.status = "approved"
        req.save()

        # 2️⃣ Notify animals_service via CONSUL (safe call)
        try:
            animals_url = get_service_url("animals-service")

            if animals_url:
                requests.post(
                    f"{animals_url}/api/animals/{req.animal_id}/adopted/",
                    timeout=3
                )
                print("✅ Animal marked as adopted:", req.animal_id)
            else:
                print("⚠ animals-service not found in Consul")

        except Exception as e:
            print("⚠ Error notifying animals_service:", e)

        # 3️⃣ RabbitMQ event (keep your logic)
        try:
            publish_adoption({
                "event": "adoption_approved",
                "request_id": req.id,
                "user_id": req.user_id,
                "animal_id": req.animal_id
            })
            print("🔔 Adoption approved event sent:", req.id)

        except Exception as e:
            print("⚠ RabbitMQ ERROR on approve:", e)

        return redirect("/adoption/admin/requests/")

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)


# -------------------------------------------------------------------
# REJECT REQUEST (FIXED)
# -------------------------------------------------------------------
def reject_request(request, id):
    try:
        req = AdoptionRequest.objects.get(id=id)
        req.status = "rejected"
        req.save()

        # Try sending event but DO NOT BREAK if RabbitMQ fails
        try:
            publish_adoption({
                "event": "adoption_rejected",
                "request_id": req.id,
                "user_id": req.user_id,
                "animal_id": req.animal_id
            })
        except Exception as e:
            print("⚠ RabbitMQ ERROR on reject:", e)

        return redirect("/adoption/admin/requests/")

    except AdoptionRequest.DoesNotExist:
        return JsonResponse({"error": "Request not found"}, status=404)


# -------------------------------------------------------------------
# API: CHECK ADOPTION
# -------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def check_adoption(request, user_id, animal_id):
    try:
        req = AdoptionRequest.objects.filter(
            user_id=user_id,
            animal_id=animal_id
        ).latest("date_requested")

        return Response({"status": req.status})
    except AdoptionRequest.DoesNotExist:
        return Response({"status": "none"}, status=404)
    
    

from adoption_service.utils import get_service_url
from django.conf import settings
def go_to_notifications(request, user_id):
    # 1. Obtenir l’URL du microservice via Consul
    notif_url = get_service_url("notifications-service")

    if notif_url is None:
        return JsonResponse({"error": "Notifications service not found in Consul"}, status=500)

    # 2. Rediriger vers notifications-service
    return redirect(
        f"{settings.TRAEFIK_BASE_URL}/notifications/user/{user_id}/"
    )