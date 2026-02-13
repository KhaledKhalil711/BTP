from django.shortcuts import render, redirect, get_object_or_404
from .forms import InscriptionForm, ContactForm, AppointmentForm, FollowUpEmailForm
from .models import Appointment, SentEmail
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.cache import cache
from datetime import datetime, time, timedelta
from functools import wraps
import logging
import json

# Rate limiting constants
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 300  # 5 minutes

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


# --- User appointments view ---

from django.contrib.auth.decorators import login_required

@login_required(login_url='/connexion/')
def mes_rendez_vous(request):
    """Show logged-in user's own appointments."""
    appointments = Appointment.objects.filter(user=request.user).order_by('-appointment_date', '-appointment_time')
    return render(request, 'core/mes_rendez_vous.html', {'appointments': appointments})


# --- Staff-required decorator ---

def staff_required(view_func):
    """Decorator that ensures user is logged in AND is_staff."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/connexion/?next={request.path}')
        if not request.user.is_staff:
            messages.error(request, "Accès non autorisé.")
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper


# --- Authentication views ---

def _get_client_ip(request):
    """Extract the client IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def connexion_view(request):
    """Handle user login with rate limiting. Staff users are redirected to dashboard."""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard_home')
        return redirect('index')

    if request.method == 'POST':
        ip = _get_client_ip(request)
        cache_key = f'login_attempts_{ip}'
        attempts = cache.get(cache_key, 0)

        if attempts >= MAX_LOGIN_ATTEMPTS:
            messages.error(request, "Trop de tentatives de connexion. Veuillez réessayer dans 5 minutes.")
            return render(request, 'core/connexion.html')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            cache.delete(cache_key)
            login(request, user)
            next_url = request.GET.get('next', '')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            if user.is_staff:
                return redirect('dashboard_home')
            return redirect('index')
        else:
            cache.set(cache_key, attempts + 1, LOGIN_LOCKOUT_SECONDS)
            remaining = MAX_LOGIN_ATTEMPTS - attempts - 1
            if remaining > 0:
                messages.error(request, f"Identifiants incorrects. {remaining} tentative(s) restante(s).")
            else:
                messages.error(request, "Trop de tentatives de connexion. Veuillez réessayer dans 5 minutes.")

    return render(request, 'core/connexion.html')


@require_http_methods(["POST"])
def deconnexion_view(request):
    """Log out the user and redirect to homepage."""
    logout(request)
    return redirect('index')


# --- Dashboard views ---

@staff_required
def dashboard_home(request):
    """Main dashboard page showing all appointments and stats."""
    appointments = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')

    context = {
        'appointments': appointments,
        'total_count': appointments.count(),
        'pending_count': appointments.filter(status='pending').count(),
        'confirmed_count': appointments.filter(status='confirmed').count(),
        'formation_count': appointments.filter(appointment_type='formation').count(),
        'livrables_count': appointments.filter(appointment_type='livrables').count(),
    }
    return render(request, 'core/dashboard/dashboard_home.html', context)


@staff_required
def dashboard_send_email(request, pk):
    """Send a follow-up email for a specific appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    sent_emails = appointment.sent_emails.all()

    if request.method == 'POST':
        form = FollowUpEmailForm(request.POST)
        if form.is_valid():
            try:
                subject = form.cleaned_data['email_subject'].replace('\n', '').replace('\r', '')
                body = form.cleaned_data['email_body']

                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[appointment.email],
                    fail_silently=False,
                )

                SentEmail.objects.create(
                    appointment=appointment,
                    subject=subject,
                    body=body,
                    recipient_email=appointment.email,
                    sent_by=request.user,
                )

                messages.success(request, f"Email envoyé avec succès à {appointment.name} ({appointment.email})")
                logger.info(f"Follow-up email sent to {appointment.email} by {request.user.username}")
                return redirect('dashboard_home')
            except Exception as e:
                logger.error(f"Error sending email: {str(e)}")
                messages.error(request, "Erreur lors de l'envoi de l'email. Veuillez réessayer.")
    else:
        form = FollowUpEmailForm(initial={
            'email_subject': f"Suite à votre rendez-vous - Gourmelon BTP",
        })

    return render(request, 'core/dashboard/send_email.html', {
        'appointment': appointment,
        'form': form,
        'sent_emails': sent_emails,
    })


@staff_required
@require_http_methods(["POST"])
def dashboard_update_status(request, pk):
    """Update the status of an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = dict(Appointment.STATUS_CHOICES)

    if new_status in valid_statuses:
        Appointment.objects.filter(pk=pk).update(status=new_status)
        appointment.refresh_from_db()
        messages.success(request, f"Statut mis à jour : {appointment.get_status_display()}")
        logger.info(f"Appointment {pk} status updated to {new_status} by {request.user.username}")
    else:
        messages.error(request, "Statut invalide.")

    return redirect('dashboard_home')


# --- Password change views ---

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin that requires user to be logged in and is_staff."""
    login_url = '/connexion/'

    def test_func(self):
        return self.request.user.is_staff


class DashboardPasswordChangeView(StaffRequiredMixin, PasswordChangeView):
    """Password change view for dashboard users."""
    template_name = 'core/dashboard/password_change.html'
    success_url = reverse_lazy('dashboard_password_done')


class DashboardPasswordDoneView(StaffRequiredMixin, PasswordChangeDoneView):
    """Password change success view for dashboard users."""
    template_name = 'core/dashboard/password_change_done.html'