from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Meep




class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class MeepForm(forms.ModelForm):
    body = forms.CharField(required=True, 
            widget = forms.widgets.Textarea(
                attrs={
                    'class': 'form-control',
                    'class': 'bg-info',
                    'class': 'py-3',
                    'placeholder':'Enter your meep!',
                }
            ),
            label='',
    )

    class Meta:
        model = Meep
        exclude = ['user',]
