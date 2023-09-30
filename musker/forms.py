from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Meep




class RegisterForm(UserCreationForm):
    #way to create any customized field in the form, and adding class, etc. 
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address',}))

    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name',}))

    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name',}))

    # Note: username and password field cannot put created as shown above since django has build in configuration for that which cannot be changed. 

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)
    
    #method to modify class, etc of password and username
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['username'].label = '' 
        self.fields['username'].help_text = '150 charters and below'

        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='Password'
        self.fields['password1'].label = '' 
        self.fields['password1'].help_text = '<strong>Case sensitive</strong>'

        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='Confirm password'
        self.fields['password2'].label = '' 
        self.fields['password2'].help_text = '<strong>Case sensitive</strong>'


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
