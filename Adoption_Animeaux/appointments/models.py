from django.db import models
from django.conf import settings
from animals.models import Animal

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)
