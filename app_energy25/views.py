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

def produkcja_wiatrowa(request):
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
    return render(request, 'app_energy25/produkcja_wiatrowa.html', context)

def suma_wiatrowa(request):
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
    return render(request, 'app_energy25/suma_wiatrowa.html', context)

def lokalizacje_wiatrowe(request):
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
    return render(request, 'app_energy25/lokalizacje_wiatrowe.html', context)

def naslonecznienie(request):
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
    return render(request, 'app_energy25/naslonecznienie.html', context)

def produkcja_pv(request):
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
    return render(request, 'app_energy25/produkcja_pv.html', context)

def suma_pv(request):
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
    return render(request, 'app_energy25/suma_pv.html', context)

def lokalizacje_pv(request):
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
    return render(request, 'app_energy25/lokalizacje_pv.html', context)