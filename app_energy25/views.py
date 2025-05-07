from django.shortcuts import render

def home(request):

    return render(request, 'app_energy25/home_page.html')
