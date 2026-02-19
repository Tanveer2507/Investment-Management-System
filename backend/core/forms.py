"""
Forms for the Investment Management System.
"""
from django import forms
from .models import Startup, Investment
from .models import Document
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """Form to edit basic user profile fields."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
        }

class StartupForm(forms.ModelForm):
    """
    Form for creating and updating Startup instances.
    """
    class Meta:
        model = Startup
        fields = [
            'name', 'image', 'description', 'industry', 'founder', 
            'founded_date', 'contact_email', 'website'
        ]
        labels = {
            'name': 'Startup Name',
            'image': 'Startup Logo / Image',
            'description': 'Description',
            'industry': 'Industry',
            'founder': 'Founder Name',
            'founded_date': 'Founded Date',
            'contact_email': 'Contact Email',
            'website': 'Website',
        }
        help_texts = {
            'description': 'Briefly describe what the startup does (2-4 sentences).',
            'image': 'Upload a high-quality image (JPG, PNG). Max recommended size 2MB.',
        }
        widgets = {
            'founded_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Startup Name', 'required': True}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Industry', 'required': True}),
            'founder': forms.TextInput(attrs={'class': 'form-control', 'aria-label': 'Founder Name', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'aria-label': 'Description', 'required': True}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'aria-label': 'Startup Image'}),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'founder@example.com',
                'aria-label': 'Contact Email'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
                'aria-label': 'Website URL'
            }),
        }

class InvestmentForm(forms.ModelForm):
    """
    Form for creating Investment instances.
    """
    class Meta:
        model = Investment
        fields = ['startup', 'amount', 'date', 'stage', 'equity_percentage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'startup': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'stage': forms.Select(attrs={'class': 'form-select'}),
            'equity_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Document title'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (optional)'}),
        }
