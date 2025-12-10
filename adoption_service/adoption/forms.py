from django import forms
from .models import AdoptionRequest

class AdoptionRequestForm(forms.ModelForm):
    class Meta:
        model = AdoptionRequest
        fields = ['user_id', 'animal_id', 'status']
        widgets = {
            'user_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'animal_id': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user_id': 'User ID',
            'animal_id': 'Animal ID',
            'status': 'Status',
        }