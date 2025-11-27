from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["name", "race", "category", "age", "description", "photo", "available"]
