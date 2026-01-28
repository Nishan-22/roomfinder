from django import forms
from .models import Room
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room    
        exclude = ['owner', 'created_at']
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']