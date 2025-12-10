from django.contrib import admin
from .models import Animal

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'breed', 'age', 'status', 'created_at')
    search_fields = ('name', 'breed', 'type', 'description')
    list_filter = ('status', 'type', 'vaccinated', 'sterilized', 'dewormed')
