from django import forms
from FS.models import FS , UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password...'}))

    class Meta():
        model = User
        fields = ('username' ,'first_name','last_name' ,'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enter username...' }),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter first name...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter last name...'}),
            'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter E-mail...'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password...'}),
            

        }

class FSForm(forms.ModelForm):
    class Meta():
        model = FS
        fields = '__all__'
        
