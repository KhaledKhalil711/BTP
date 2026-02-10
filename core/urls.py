from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('formation/', views.formation, name='formation'),
    path('livrables/', views.livrables, name='livrables'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription, name='inscription'),
    # API endpoints
    path('api/available-slots/', views.get_available_slots, name='api_available_slots'),
    # Authentication
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='dashboard_logout'),
    # Client Dashboard
    path('tableau-de-bord/', views.dashboard_home, name='dashboard_home'),
    path('tableau-de-bord/rendez-vous/<int:pk>/email/', views.dashboard_send_email, name='dashboard_send_email'),
    path('tableau-de-bord/rendez-vous/<int:pk>/statut/', views.dashboard_update_status, name='dashboard_update_status'),
    path('tableau-de-bord/mot-de-passe/', views.DashboardPasswordChangeView.as_view(), name='dashboard_password_change'),
    path('tableau-de-bord/mot-de-passe/fait/', views.DashboardPasswordDoneView.as_view(), name='dashboard_password_done'),
]
