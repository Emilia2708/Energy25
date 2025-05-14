from django.shortcuts import render

def home(request):

    return render(request, 'app_energy25/home_page.html')

def predkosc_wiatru(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/predkosc_wiatru.html', context)

def produkcja_wiatrowa(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/produkcja_wiatrowa.html', context)

def suma_wiatrowa(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_wiatrowa.html', context)

def lokalizacje_wiatrowe(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/lokalizacje_wiatrowe.html', context)

def naslonecznienie(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/naslonecznienie.html', context)

def produkcja_pv(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/produkcja_pv.html', context)

def suma_pv(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_pv.html', context)

def lokalizacje_pv(request):
    years_list = [
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020",
        "2021",
        "2022",
        "2024",
    ]
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/lokalizacje_pv.html', context)