from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing'), # Point root to index directly
    # path('index/', views.index, name='index'), # Removed to avoid confusion/redundancy, or can keep as alias
    path('formation/', views.formation, name='formation'),
    path('livrables/', views.livrables, name='livrables'),
]
