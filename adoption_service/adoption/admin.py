from django.contrib import admin
from .models import AdoptionRequest

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'animal_id', 'status', 'date_requested')
    list_filter = ('status', 'date_requested')
