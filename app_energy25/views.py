from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from wykresy.wykres_produkcja_pv import AnalizaEnergiiPV
import json
import logging
import plotly.graph_objects as go
from plotly.offline import plot  # Importuj plot z plotly.offline

# Konfiguracja logowania
logger = logging.getLogger(__name__)

def wczytaj_dane_pv():
    """
    Wczytuje dane PV z bazy danych PostgreSQL.
    Obsługuje błędy połączenia i zapytania, loguje je i zwraca None w przypadku niepowodzenia.
    """
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query = text("SELECT * FROM wpisy_pv_pogoda")
        wpisy_pv_pogoda = pd.read_sql_query(query, engine)
        logger.info("Dane PV pomyślnie pobrane z bazy danych.")
        return wpisy_pv_pogoda
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas pobierania danych z bazy danych: {e}", exc_info=True)
        return None
    finally:
        if engine:
            engine.dispose()

def produkcja_pv(request):
    """
    Wyświetla stronę z wykresem produkcji PV.
    """
    years_list = list(range(2015, 2024))
    df_pv = wczytaj_dane_pv()  # Pobierz dane PV
    if df_pv is None:
        return render(request, 'app_energy25/produkcja_pv.html', {'error': 'Nie udało się pobrać danych PV z bazy danych'},)

    analiza_pv = AnalizaEnergiiPV(df_pv)
    suma_energii = analiza_pv._oblicz_sume_energii()

    # Tworzenie wykresu Plotly
    fig_pv = go.Figure()
    for rok, grupa in suma_energii.groupby(level=0):
        fig_pv.add_trace(go.Scatter(x=grupa.index.get_level_values(1), y=grupa.values, mode='lines', name=str(rok)))
    fig_pv.update_layout(
        title='Energia wyprodukowana w elektrowniach słonecznych',
        xaxis_title='Miesiąc',
        yaxis_title='Suma energii (MWh)',
        height=600,  # Dodano ustawienie wysokości
        width=800,   # Dodano ustawienie szerokości
    )

    # Konwertuj wykres na HTML i przekaż do szablonu
    plot_html = plot(fig_pv, output_type='div')

    context = {
        'years': years_list,
        'plot_html': plot_html,  # Dodano 'plot_html' do kontekstu
    }
    return render(request, 'app_energy25/produkcja_pv.html', context)


@csrf_exempt
def pobierz_dane_pv(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            logger.debug(f"Wybrane lata: {selected_years}")

            df_pv = wczytaj_dane_pv()
            logger.debug(f"Dane PV pobrane z bazy danych: {df_pv.head().to_string() if df_pv is not None else None}")

            if df_pv is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych PV z bazy danych. Sprawdź logi serwera.'}, status=500)

            analiza_pv = AnalizaEnergiiPV(df_pv)
            dane_wykresu = analiza_pv.pobierz_dane_dla_lat(selected_years)
            logger.debug(f"Dane wykresu po przetworzeniu: {dane_wykresu}")

            logger.info("Dane wykresu PV pomyślnie wygenerowane i zwrócone.")
            return JsonResponse(dane_wykresu)
        except json.JSONDecodeError as e:
            logger.error(f"Błąd dekodowania JSON: {e}", exc_info=True)
            return JsonResponse({'error': 'Nieprawidłowy format JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Wystąpił błąd podczas przetwarzania żądania: {e}", exc_info=True)
            return JsonResponse({'error': 'Wystąpił błąd serwera.'}, status=500)
    else:
        return JsonResponse({'error': 'Dozwolona jest tylko metoda POST.'}, status=405)

def home(request):
    """
    Wyświetla stronę główną.
    """
    return render(request, 'app_energy25/home_page.html')

def generuj_widok_z_latami(request, szablon):
    """
    Generuje widok z listą lat 2015-2024.
    """
    years_list = list(range(2015, 2024))
    context = {
        'years': years_list,
    }
    return render(request, f'app_energy25/{szablon}.html', context)

def predkosc_wiatru(request):
    """
    Wyświetla stronę z wyborem lat do analizy prędkości wiatru.
    """
    return generuj_widok_z_latami(request, 'predkosc_wiatru')

def produkcja_wiatrowa(request):
    """
    Wyświetla stronę z wyborem lat do analizy produkcji wiatrowej.
    """
    return generuj_widok_z_latami(request, 'produkcja_wiatrowa')

def suma_wiatrowa(request):
    """
    Wyświetla stronę z wyborem lat do analizy sumy produkcji wiatrowej.
    """
    return generuj_widok_z_latami(request, 'suma_wiatrowa')

def lokalizacje_wiatrowe(request):
    """
    Wyświetla stronę z wyborem lat do analizy lokalizacji wiatrowych.
    """
    return generuj_widok_z_latami(request, 'lokalizacje_wiatrowe')

def naslonecznienie(request):
    """
    Wyświetla stronę z wyborem lat do analizy nasłonecznienia.
    """
    return generuj_widok_z_latami(request, 'naslonecznienie')

def suma_pv(request):
    """
    Wyświetla stronę z wyborem lat do analizy sumy produkcji PV.
    """
    return generuj_widok_z_latami(request, 'suma_pv')

def lokalizacje_pv(request):
    """
    Wyświetla stronę z wyborem lat do analizy lokalizacji PV.
    """
    return generuj_widok_z_latami(request, 'lokalizacje_pv')
