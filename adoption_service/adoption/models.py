from django.db import models

class AdoptionRequest(models.Model):
    user_id = models.IntegerField()
    animal_id = models.IntegerField()
    appointment_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default="pending") 
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adoption user {self.user_id} → animal {self.animal_id}"
