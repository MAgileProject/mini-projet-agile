from django.db import models

class Animal(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending Approval'),
    ]

    name = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    breed = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    size = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    vaccinated = models.BooleanField(default=False)
    sterilized = models.BooleanField(default=False)
    dewormed = models.BooleanField(default=False)
    medical_conditions = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="available")
    photo_url = models.URLField(blank=True)
    submitted_by_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
