
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from shared.consul_client import get_service_url
from django.shortcuts import render, redirect
from shared.consul_client import get_service_url

def home(request):
    return render(request, "home.html")

def go_animals(request):
    url = get_service_url("animals-service")
    return redirect(url)
