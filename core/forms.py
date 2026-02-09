from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactMessage, Appointment
from datetime import datetime, timedelta


class ContactForm(forms.ModelForm):
    """Form for handling contact submissions with validation."""

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre message', 'rows': 5}),
        }
        labels = {
            'name': 'Nom',
            'email': 'Email',
            'subject': 'Sujet',
            'message': 'Message',
        }


class InscriptionForm(UserCreationForm):
    """Form for user registration with extended fields."""

    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(max_length=254, required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class AppointmentForm(forms.ModelForm):
    """Form for booking appointments (rendez-vous)."""

    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'appointment_date', 'appointment_time', 'subject', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom complet',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'votre.email@exemple.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+33 6 12 34 56 78',
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sujet du rendez-vous',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Informations complémentaires ou demandes spéciales',
                'rows': 4
            }),
        }
        labels = {
            'name': 'Nom complet',
            'email': 'Email',
            'phone': 'Téléphone',
            'appointment_date': 'Date',
            'appointment_time': 'Heure',
            'subject': 'Sujet',
            'notes': 'Notes',
        }

    def clean_appointment_date(self):
        """Validate that appointment date is not in the past and is a weekday."""
        date = self.cleaned_data.get('appointment_date')
        if date:
            # Check if date is in the past
            if date < datetime.now().date():
                raise forms.ValidationError("La date du rendez-vous ne peut pas être dans le passé.")

            # Check if date is on weekend
            if date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                raise forms.ValidationError("Les rendez-vous ne sont disponibles que du lundi au vendredi.")

        return date

    def clean_appointment_time(self):
        """Validate that appointment time is within business hours."""
        time = self.cleaned_data.get('appointment_time')
        if time:
            if time.hour < 9 or time.hour >= 16:
                raise forms.ValidationError("Les rendez-vous sont disponibles de 9h à 16h.")
        return time
