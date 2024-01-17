from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User 

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

    class Meta:
        model = User
        fields=['username','password1','password2','first_name','last_name','email','birth_date']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }
