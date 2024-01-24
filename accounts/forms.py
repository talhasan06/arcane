from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError
from datetime import date

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        label='Birth date',
         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Check if the user is at least 18 years old
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                raise ValidationError('You must be at least 18 years old to register.')

        return birth_date
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
