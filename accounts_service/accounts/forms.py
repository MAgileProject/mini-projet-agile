from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "phone", "address", "password"]


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "autocomplete": "new-email"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "autocomplete": "new-password"
    }))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["firstname", "lastname", "email", "phone", "address"]
