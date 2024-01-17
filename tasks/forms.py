# forms.py

from django import forms
from .models import Task,Category

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date','due_time','priority','category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
