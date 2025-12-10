from rest_framework import serializers
from .models import AdoptionRequest


class AdoptionRequestSerializer(serializers.ModelSerializer):
 class Meta:
   model = AdoptionRequest
   fields = ['id', 'user_id', 'animal_id', 'date', 'status']
   read_only_fields = ['id', 'date']