from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # Root path serves index.html
    # path('index/', views.index, name='index'), # Removed to avoid confusion/redundancy, or can keep as alias
    path('formation/', views.formation, name='formation'),
    path('livrables/', views.livrables, name='livrables'),
]
