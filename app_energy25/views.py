from django.shortcuts import render

def home(request):

    return render(request, 'app_energy25/home_page.html')

def predkosc_wiatru(request):
    months_list = [
        "Styczeń",
        "Luty",
        "Marzec",
        "Kwiecień",
        "Maj",
        "Czerwiec",
        "Lipiec",
        "Sierpień",
        "Wrzesień",
        "Październik",
        "Listopad",
        "Grudzień",
    ]
    context = {
        'months': months_list,
    }
    return render(request, 'app_energy25/predkosc_wiatru.html', context)
