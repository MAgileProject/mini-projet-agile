from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='animals/', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
