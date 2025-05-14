from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from wykresy.wykres_produkcja_pv import AnalizaEnergiiPV
import json

def wczytaj_dane_pv():
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    try:
        wpisy_pv_pogoda = pd.read_sql_table('wpisy_pv_pogoda', engine)
    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania danych z bazy danych: {e}")
        return None
    finally:
        engine.dispose()
    return wpisy_pv_pogoda

def produkcja_pv(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/produkcja_pv.html', context)

@csrf_exempt
def pobierz_dane_pv(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            print("Wybrane lata:", selected_years)

            df_pv = wczytaj_dane_pv()
            if df_pv is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych PV z bazy danych'}, status=500)

            analiza_pv = AnalizaEnergiiPV(df_pv)
            dane_wykresu = analiza_pv.pobierz_dane_dla_lat(selected_years)

            return JsonResponse(dane_wykresu)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Nieprawidłowy format JSON'}, status=400)
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania żądania: {e}")
            return JsonResponse({'error': f'Wystąpił błąd serwera: {e}'}, status=500)
    else:
        return JsonResponse({'error': 'Dozwolona tylko metoda POST'}, status=405)

def home(request):
    return render(request, 'app_energy25/home_page.html')

def predkosc_wiatru(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/predkosc_wiatru.html', context)

def produkcja_wiatrowa(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/produkcja_wiatrowa.html', context)

def suma_wiatrowa(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_wiatrowa.html', context)

def lokalizacje_wiatrowe(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/lokalizacje_wiatrowe.html', context)

def naslonecznienie(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/naslonecznienie.html', context)

def suma_pv(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_pv.html', context)

def lokalizacje_pv(request):
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/lokalizacje_pv.html', context)