from django.contrib import admin
from .models import ContactMessage, Appointment, SentEmail


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for contact messages."""
    list_display = ("name", "email", "subject", "sent_at")
    list_filter = ("sent_at",)
    search_fields = ("name", "email", "subject", "message")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin interface for appointments."""
    list_display = ("name", "email", "appointment_type", "appointment_date", "appointment_time", "status", "created_at")
    list_filter = ("appointment_type", "status", "appointment_date", "created_at")
    search_fields = ("name", "email", "phone", "subject", "notes")
    date_hierarchy = "appointment_date"
    ordering = ("-appointment_date", "-appointment_time")

    fieldsets = (
        ("Informations du client", {
            "fields": ("user", "name", "email", "phone")
        }),
        ("Détails du rendez-vous", {
            "fields": ("appointment_type", "appointment_date", "appointment_time", "duration_hours", "subject", "notes")
        }),
        ("Statut", {
            "fields": ("status",)
        }),
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(SentEmail)
class SentEmailAdmin(admin.ModelAdmin):
    """Admin interface for sent follow-up emails."""
    list_display = ("recipient_email", "subject", "sent_at", "sent_by")
    list_filter = ("sent_at",)
    search_fields = ("recipient_email", "subject", "body")
    readonly_fields = ("appointment", "subject", "body", "recipient_email", "sent_at", "sent_by")
