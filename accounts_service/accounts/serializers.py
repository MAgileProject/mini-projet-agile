from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "firstname",
            "lastname",
            "email",
            "phone",
            "address",
            "is_admin",
            "is_active",
            "created_at",
            "updated_at",
        ]
