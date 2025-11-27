from django.db import models
from django.conf import settings
from animals.models import Animal

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending','En attente'),
        ('accepted','Acceptée'),
        ('rejected','Refusée'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.animal} ({self.status})"
