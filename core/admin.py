from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "sent_at")
    list_filter = ("sent_at",)
    search_fields = ("name", "email", "subject", "message")

# Register your models here.
