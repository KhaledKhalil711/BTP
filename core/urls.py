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
]
