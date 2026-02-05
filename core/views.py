from django.shortcuts import render
from django.contrib import messages
from .models import ContactMessage
def landing(request):
    return render(request, 'core/landing.html')

def index(request):
    return render(request, 'core/index.html')

def formation(request):
    return render(request, 'core/formation.html')

def livrables(request):
    return render(request, 'core/livrables.html')

def contact(request):
    return render(request, 'core/contact.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message_text = request.POST.get("message")

        # Enregistrer le message dans la base
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        messages.success(request, "Message envoyé avec succès !")

    return render(request, "core/contact.html")