from django.shortcuts import render

def home(request):

    return render(request, 'app_energy25/home_page.html')

def predkosc_wiatru(request):

    return render(request, 'app_energy25/predkosc_wiatru.html')
