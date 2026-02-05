from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def formation(request):
    return render(request, 'core/formation.html')

def livrables(request):
    return render(request, 'core/livrables.html')
