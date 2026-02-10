"""Models for the core application."""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time, datetime


class ContactMessage(models.Model):
    """Model to store contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Appointment(models.Model):
    """Model to store rendez-vous bookings for formations and livrables."""

    APPOINTMENT_TYPE_CHOICES = [
        ('formation', 'Formation'),
        ('livrables', 'Livrables'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]

    # User information (can be null if user not registered)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    name = models.CharField(max_length=100, help_text="Nom complet")
    email = models.EmailField(help_text="Email de contact")
    phone = models.CharField(max_length=20, blank=True, help_text="Numéro de téléphone")

    # Appointment details
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES)
    appointment_date = models.DateField(help_text="Date du rendez-vous")
    appointment_time = models.TimeField(help_text="Heure du rendez-vous")
    duration_hours = models.IntegerField(default=1, help_text="Durée en heures")

    # Additional information
    subject = models.CharField(max_length=200, blank=True, help_text="Sujet du rendez-vous")
    notes = models.TextField(blank=True, help_text="Notes ou demandes spéciales")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date', 'appointment_time']
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        unique_together = ['appointment_type', 'appointment_date', 'appointment_time']

    def __str__(self):
        return f"{self.get_appointment_type_display()} - {self.name} - {self.appointment_date} à {self.appointment_time}"

    def clean(self):
        """Validate appointment time is within business hours (9:00-16:00)."""
        if self.appointment_time:
            if self.appointment_time < time(9, 0) or self.appointment_time >= time(16, 0):
                raise ValidationError("Les rendez-vous sont disponibles de 9h à 16h du lundi au vendredi.")

        # Check if appointment is on weekend
        if self.appointment_date:
            if self.appointment_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                raise ValidationError("Les rendez-vous ne sont disponibles que du lundi au vendredi.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SentEmail(models.Model):
    """Model to track follow-up emails sent from the dashboard."""

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='sent_emails')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    recipient_email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Email envoyé'
        verbose_name_plural = 'Emails envoyés'

    def __str__(self):
        return f"Email à {self.recipient_email} - {self.subject} ({self.sent_at.strftime('%d/%m/%Y')})"
