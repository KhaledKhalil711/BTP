from django.urls import path
from . import views
from .views import contact
urlpatterns = [
    path('', views.index, name='index'), # Root path serves index.html
    # path('index/', views.index, name='index'), # Removed to avoid confusion/redundancy, or can keep as alias
    path('formation/', views.formation, name='formation'),
    path('livrables/', views.livrables, name='livrables'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription, name='inscription'),
]
