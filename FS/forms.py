from django import forms
from FS.models import FS , UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-check-input','placeholder':'enter Password...'}))

    class Meta():
        model = User
        fields = ('username' ,'first_name','last_name' ,'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'enter username...' }),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter first name...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter last name...'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'enter E-mail...'}),
            

        }

class FSForm(forms.ModelForm):
    class Meta():
        model = FS
        fields = '__all__'
        
