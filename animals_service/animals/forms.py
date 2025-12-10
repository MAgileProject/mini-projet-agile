from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name', 'age', 'type', 'breed', 'gender', 'size',
            'description', 'vaccinated', 'sterilized', 'dewormed',
            'medical_conditions', 'location', 'photo_url'
        ]
