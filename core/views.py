from django.shortcuts import render, redirect
from .forms import InscriptionForm, ContactForm, AppointmentForm
from .models import Appointment
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime, time, timedelta
import logging
import json

logger = logging.getLogger(__name__)


def landing(request):
    """Render the landing page."""
    return render(request, 'core/landing.html')


def index(request):
    """Render the index/portfolio page."""
    return render(request, 'core/index.html')


def formation(request):
    """
    Render the training programs page with booking functionality.
    GET: Display formations and booking form
    POST: Process booking submission
    """
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.appointment_type = 'formation'
                if request.user.is_authenticated:
                    appointment.user = request.user
                appointment.save()
                messages.success(request, "Votre rendez-vous pour la formation a été enregistré avec succès ! Nous vous contacterons bientôt.")
                logger.info(f"Formation appointment booked: {appointment.name} - {appointment.appointment_date} at {appointment.appointment_time}")
                return redirect('formation')
            except Exception as e:
                logger.error(f"Error booking formation appointment: {str(e)}")
                messages.error(request, "Une erreur s'est produite lors de la réservation. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = AppointmentForm()

    return render(request, 'core/formation.html', {'form': form})


def livrables(request):
    """
    Render the deliverables/projects page with booking functionality.
    GET: Display livrables and booking form
    POST: Process booking submission
    """
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment = form.save(commit=False)
                appointment.appointment_type = 'livrables'
                if request.user.is_authenticated:
                    appointment.user = request.user
                appointment.save()
                messages.success(request, "Votre rendez-vous pour les livrables a été enregistré avec succès ! Nous vous contacterons bientôt.")
                logger.info(f"Livrables appointment booked: {appointment.name} - {appointment.appointment_date} at {appointment.appointment_time}")
                return redirect('livrables')
            except Exception as e:
                logger.error(f"Error booking livrables appointment: {str(e)}")
                messages.error(request, "Une erreur s'est produite lors de la réservation. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = AppointmentForm()

    return render(request, 'core/livrables.html', {'form': form})


def contact(request):
    """
    Handle contact form submission.
    GET: Display contact form
    POST: Process and save contact message
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Message envoyé avec succès !")
                logger.info(f"Contact message received from {form.cleaned_data['email']}")
                return redirect('contact')
            except Exception as e:
                logger.error(f"Error saving contact message: {str(e)}")
                messages.error(request, "Une erreur s'est produite. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = ContactForm()

    return render(request, "core/contact.html", {'form': form})


def inscription(request):
    """
    Handle user registration.
    GET: Display registration form
    POST: Process and create new user account
    """
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, "Inscription réussie ! Bienvenue.")
                logger.info(f"New user registered: {user.username}")
                return redirect('index')
            except Exception as e:
                logger.error(f"Error during registration: {str(e)}")
                messages.error(request, "Une erreur s'est produite lors de l'inscription.")
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = InscriptionForm()

    return render(request, 'core/inscription.html', {'form': form})


@require_http_methods(["GET"])
def get_available_slots(request):
    """
    API endpoint to get available time slots for a specific date and appointment type.
    Query params: date (YYYY-MM-DD), type (formation|livrables)
    """
    try:
        date_str = request.GET.get('date')
        appointment_type = request.GET.get('type')

        if not date_str or not appointment_type:
            return JsonResponse({'error': 'Date and type parameters are required'}, status=400)

        # Parse the date
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Check if date is valid (not weekend, not in past)
        if appointment_date.weekday() >= 5:
            return JsonResponse({'error': 'Les rendez-vous ne sont disponibles que du lundi au vendredi.'}, status=400)

        if appointment_date < datetime.now().date():
            return JsonResponse({'error': 'La date ne peut pas être dans le passé.'}, status=400)

        # Get all booked appointments for this date and type
        booked_appointments = Appointment.objects.filter(
            appointment_date=appointment_date,
            appointment_type=appointment_type,
            status__in=['pending', 'confirmed']
        ).values_list('appointment_time', flat=True)

        booked_times = set(booked_appointments)

        # Generate all possible time slots (9:00 to 15:00, each hour)
        available_slots = []
        for hour in range(9, 16):  # 9 to 15 (last slot at 15:00)
            slot_time = time(hour, 0)
            if slot_time not in booked_times:
                available_slots.append({
                    'time': slot_time.strftime('%H:%M'),
                    'display': f"{hour}:00 - {hour+1}:00"
                })

        return JsonResponse({
            'date': date_str,
            'type': appointment_type,
            'available_slots': available_slots
        })

    except ValueError as e:
        logger.error(f"Invalid date format: {str(e)}")
        return JsonResponse({'error': 'Format de date invalide. Utilisez YYYY-MM-DD.'}, status=400)
    except Exception as e:
        logger.error(f"Error fetching available slots: {str(e)}")
        return JsonResponse({'error': 'Une erreur s\'est produite.'}, status=500)