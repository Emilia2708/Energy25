# app_energy25/views.py

import pandas as pd
import folium
import re
import os
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import json
import logging
from wykresy.wykres_produkcja_pv import AnalizaEnergiiPV
from wykresy.wykres_produkcja_wil import AnalizaEnergiiWil
from wykresy.wykres_predkosc_wiatru import PredkoscWiatru
from wykresy.naslonecznienie import Naslonecznienie
from wykresy.wykres_suma_pv import SumaPV

# Konfiguracja logowania
logger = logging.getLogger(__name__)


# --- Istniejące funkcje wczytywania danych (pozostają bez zmian) ---
def wczytaj_dane_pv():
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
        if 'engine' in locals() and engine:
            engine.dispose()


def wczytaj_dane_wil():
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query = text("SELECT * FROM wpisy_wil_pogoda")
        wpisy_wil_pogoda = pd.read_sql_query(query, engine)
        logger.info("Dane WIL pomyślnie pobrane z bazy danych.")
        return wpisy_wil_pogoda
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas pobierania danych WIL z bazy danych: {e}", exc_info=True)
        return None
    finally:
        if 'engine' in locals() and engine:
            engine.dispose()


def wczytaj_dane_wiatr():
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query = text("SELECT * FROM pogoda_wil")
        pogoda_wil = pd.read_sql_query(query, engine)
        logger.info("Dane wiatrowe pomyślnie pobrane z bazy danych.")
        return pogoda_wil
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas pobierania danych wiatrowych z bazy danych: {e}", exc_info=True)
        return None
    finally:
        if 'engine' in locals() and engine:
            engine.dispose()


def wczytaj_dane_naslonecznienie():
    load_dotenv()
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASS')
    db_host = 'localhost'
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    try:
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        query = text("SELECT * FROM pogoda_pv")
        pogoda_pv = pd.read_sql_query(query, engine)
        logger.info("Dane nasłonecznienia pomyślnie pobrane z bazy danych.")
        return pogoda_pv
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas pobierania danych nasłonecznienia z bazy danych: {e}", exc_info=True)
        return None
    finally:
        if 'engine' in locals() and engine:
            engine.dispose()


# --- Funkcja pomocnicza do konwersji DMS na Stopnie Dziesiętne (pozostaje bez zmian) ---
def dms_to_dd(dms_str):
    if pd.isna(dms_str) or not isinstance(dms_str, str):
        return None
    match = re.match(r'(\d+)[°]?(\d+\.?\d*)?[\']?([NSEW])', dms_str.strip(), re.IGNORECASE)
    if not match:
        logger.warning(f"Nie udało się sparsować wartości DMS: '{dms_str}'")
        return None
    degrees = float(match.group(1))
    minutes = float(match.group(2)) if match.group(2) else 0.0
    direction = match.group(3).upper()
    dd = degrees + minutes / 60
    if direction in ('S', 'W'):
        dd *= -1
    return dd


# --- Widok dla mapy lokalizacji PV (zmodyfikowany) ---
def lokalizacje_pv(request):
    df_pv = wczytaj_dane_pv()
    if df_pv is None:
        return render(request, 'app_energy25/lokalizacje_pv.html',
                      {'error': 'Nie udało się pobrać danych PV z bazy danych'})

    wspgeog_path = os.path.join(settings.BASE_DIR, 'app_energy25', 'data', 'wspgeog.xlsx')

    try:
        wspgeog = pd.read_excel(wspgeog_path)
        logger.info(f"Plik wspgeog.xlsx wczytany z: {wspgeog_path}")
    except FileNotFoundError:
        logger.error(f"Plik wspgeog.xlsx nie został znaleziony pod ścieżką: {wspgeog_path}")
        return render(request, 'app_energy25/lokalizacje_pv.html', {
            'error': 'Nie udało się znaleźć pliku z danymi geograficznymi (wspgeog.xlsx). Upewnij się, że znajduje się w app_energy25/data/'})
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas wczytywania wspgeog.xlsx: {e}", exc_info=True)
        return render(request, 'app_energy25/lokalizacje_pv.html',
                      {'error': f'Błąd podczas wczytywania danych geograficznych: {e}'})

    if 'Miejscowosc' not in df_pv.columns or 'Miejscowosc' not in wspgeog.columns:
        logger.error("Brak kolumny 'Miejscowosc' w jednym z dataframe'ów. Nie można połączyć.")
        return render(request, 'app_energy25/lokalizacje_pv.html',
                      {'error': "Brak kolumny 'Miejscowosc' w danych PV lub geograficznych."})

    mapa_pv_data = df_pv[['Miejscowosc']].drop_duplicates()

    mapa_pv_data = pd.merge(mapa_pv_data, wspgeog, on='Miejscowosc', how='inner')

    if mapa_pv_data.empty:
        logger.warning("Brak danych po połączeniu tabel Miejscowosc i wspgeog. Nie można wygenerować mapy.")
        return render(request, 'app_energy25/lokalizacje_pv.html', {
            'error': 'Brak danych lokalizacji do wyświetlenia na mapie. Sprawdź, czy dane Miejscowość są spójne w obu źródłach.'})

    mapa_pv_data['Szerokosc_dd'] = mapa_pv_data['Szerokosc'].apply(dms_to_dd)
    mapa_pv_data['Dlugosc_dd'] = mapa_pv_data['Dlugosc'].apply(dms_to_dd)
    mapa_pv_data = mapa_pv_data.dropna(subset=['Szerokosc_dd', 'Dlugosc_dd'])

    if mapa_pv_data.empty:
        logger.warning("Brak prawidłowych współrzędnych po konwersji DMS na DD. Nie można wygenerować mapy.")
        return render(request, 'app_energy25/lokalizacje_pv.html',
                      {'error': 'Nie udało się przetworzyć współrzędnych geograficznych. Sprawdź format danych.'})

    avg_lat = mapa_pv_data['Szerokosc_dd'].mean()
    avg_lon = mapa_pv_data['Dlugosc_dd'].mean()

    m_pv = folium.Map(location=[avg_lat, avg_lon], zoom_start=6.5)

    for index, row in mapa_pv_data.iterrows():
        folium.Marker(
            location=[row['Szerokosc_dd'], row['Dlugosc_dd']],
            popup=row['Miejscowosc'],
            icon=folium.Icon(icon="solar-panel", prefix='fa')
        ).add_to(m_pv)

    map_html = m_pv._repr_html_()

    context = {
        'map_html': map_html,
    }
    return render(request, 'app_energy25/lokalizacje_pv.html', context)


# --- NOWA FUNKCJA WIDOKU DLA LOKALIZACJI WIATROWYCH ---
def lokalizacje_wiatrowe(request):
    """
    Wyświetla stronę z mapą lokalizacji instalacji wiatrowych.
    """
    df_wil = wczytaj_dane_wil()
    if df_wil is None:
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html',
                      {'error': 'Nie udało się pobrać danych WIL z bazy danych'})

    # Ścieżka do pliku wspgeog.xlsx (tak samo jak dla PV)
    wspgeog_path = os.path.join(settings.BASE_DIR, 'app_energy25', 'data', 'wspgeog.xlsx')

    try:
        wspgeog = pd.read_excel(wspgeog_path)
        logger.info(f"Plik wspgeog.xlsx wczytany z: {wspgeog_path}")
    except FileNotFoundError:
        logger.error(f"Plik wspgeog.xlsx nie został znaleziony pod ścieżką: {wspgeog_path}")
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html', {
            'error': 'Nie udało się znaleźć pliku z danymi geograficznymi (wspgeog.xlsx). Upewnij się, że znajduje się w app_energy25/data/'})
    except Exception as e:
        logger.error(f"Wystąpił błąd podczas wczytywania wspgeog.xlsx: {e}", exc_info=True)
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html',
                      {'error': f'Błąd podczas wczytywania danych geograficznych: {e}'})

    if 'Miejscowosc' not in df_wil.columns or 'Miejscowosc' not in wspgeog.columns:
        logger.error("Brak kolumny 'Miejscowosc' w jednym z dataframe'ów. Nie można połączyć.")
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html',
                      {'error': "Brak kolumny 'Miejscowosc' w danych WIL lub geograficznych."})

    mapa_wil_data = df_wil[['Miejscowosc']].drop_duplicates()
    mapa_wil_data = pd.merge(mapa_wil_data, wspgeog, on='Miejscowosc', how='inner')

    if mapa_wil_data.empty:
        logger.warning("Brak danych po połączeniu tabel Miejscowosc i wspgeog. Nie można wygenerować mapy.")
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html', {
            'error': 'Brak danych lokalizacji do wyświetlenia na mapie. Sprawdź, czy dane Miejscowość są spójne w obu źródłach.'})

    # Konwersja współrzędnych i filtrowanie wartości None
    mapa_wil_data['Szerokosc_dd'] = mapa_wil_data['Szerokosc'].apply(dms_to_dd)
    mapa_wil_data['Dlugosc_dd'] = mapa_wil_data['Dlugosc'].apply(dms_to_dd)
    mapa_wil_data = mapa_wil_data.dropna(subset=['Szerokosc_dd', 'Dlugosc_dd'])

    if mapa_wil_data.empty:
        logger.warning("Brak prawidłowych współrzędnych po konwersji DMS na DD. Nie można wygenerować mapy.")
        return render(request, 'app_energy25/lokalizacje_wiatrowe.html',
                      {'error': 'Nie udało się przetworzyć współrzędnych geograficznych. Sprawdź format danych.'})

    # Obliczanie średniej długości i szerokości potrzebnej do wycentrowania mapy
    avg_lat = mapa_wil_data['Szerokosc_dd'].mean()
    avg_lon = mapa_wil_data['Dlugosc_dd'].mean()

    m_wil = folium.Map(location=[avg_lat, avg_lon], zoom_start=6.5)

    for index, row in mapa_wil_data.iterrows():
        folium.Marker(
            location=[row['Szerokosc_dd'], row['Dlugosc_dd']],
            popup=row['Miejscowosc'],
            icon=folium.Icon(icon="cloud", prefix='fa') # Użycie ikony "cloud"
        ).add_to(m_wil)

    # Zapisanie mapy do ciągu HTML
    map_html = m_wil._repr_html_()

    context = {
        'map_html': map_html,
    }
    return render(request, 'app_energy25/lokalizacje_wiatrowe.html', context)

# --- Pozostałe istniejące funkcje z views.py (pozostają bez zmian) ---

def produkcja_pv(request):
    years_list = list(range(2015, 2024))
    df_pv = wczytaj_dane_pv()
    if df_pv is None:
        return render(request, 'app_energy25/produkcja_pv.html',
                      {'error': 'Nie udało się pobrać danych PV z bazy danych'})
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
            logger.debug(f"Wybrane lata: {selected_years}")

            df_pv = wczytaj_dane_pv()
            logger.debug(f"Dane PV pobrane z bazy danych: {df_pv.head().to_string() if df_pv is not None else None}")

            if df_pv is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych PV z bazy danych. Sprawdź logi serwera.'},
                                    status=500)

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


def produkcja_wiatrowa(request):
    years_list = list(range(2015, 2024))
    df_wil = wczytaj_dane_wil()
    if df_wil is None:
        return render(request, 'app_energy25/produkcja_wiatrowa.html',
                      {'error': 'Nie udało się pobrać danych WIL z bazy danych'})

    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/produkcja_wiatrowa.html', context)


@csrf_exempt
def pobierz_dane_wil(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            logger.debug(f"Wybrane lata: {selected_years}")

            df_wil = wczytaj_dane_wil()
            logger.debug(f"Dane WIL pobrane z bazy danych: {df_wil.head().to_string() if df_wil is not None else None}")

            if df_wil is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych WIL z bazy danych. Sprawdź logi serwera.'},
                                    status=500)

            analiza_wil = AnalizaEnergiiWil(df_wil)
            dane_wykresu = analiza_wil.pobierz_dane_dla_lat(selected_years)
            logger.debug(f"Dane wykresu po przetworzeniu: {dane_wykresu}")

            logger.info("Dane wykresu WIL pomyślnie wygenerowane i zwrócone.")
            return JsonResponse(dane_wykresu)
        except json.JSONDecodeError as e:
            logger.error(f"Błąd dekodowania JSON: {e}", exc_info=True)
            return JsonResponse({'error': 'Nieprawidłowy format JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Wystąpił błąd podczas przetwarzania żądania: {e}", exc_info=True)
            return JsonResponse({'error': 'Wystąpił błąd serwera.'}, status=500)
    else:
        return JsonResponse({'error': 'Dozwolona jest tylko metoda POST.'}, status=405)


def predkosc_wiatru(request):
    years_list = list(range(2015, 2024))
    df_wiatr = wczytaj_dane_wiatr()
    if df_wiatr is None:
        return render(request, 'app_energy25/predkosc_wiatru.html',
                      {'error': 'Nie udało się pobrać danych WIL z bazy danych'})

    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/predkosc_wiatru.html', context)


@csrf_exempt
def pobierz_dane_wiatr(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            logger.debug(f"Wybrane lata: {selected_years}")

            df_wiatr = wczytaj_dane_wiatr()
            logger.debug(
                f"Dane wiatru pobrane z bazy danych: {df_wiatr.head().to_string() if df_wiatr is not None else None}")

            if df_wiatr is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych WIL z bazy danych. Sprawdź logi serwera.'},
                                    status=500)

            analiza_wiatr = PredkoscWiatru(df_wiatr)
            dane_wykresu = analiza_wiatr.pobierz_dane_dla_lat(selected_years)
            logger.debug(f"Dane wykresu po przetworzeniu: {dane_wykresu}")

            logger.info("Dane wykresu prędkości wiatru pomyślnie wygenerowane i zwrócone.")
            return JsonResponse(dane_wykresu)
        except json.JSONDecodeError as e:
            logger.error(f"Błąd dekodowania JSON: {e}", exc_info=True)
            return JsonResponse({'error': 'Nieprawidłowy format JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Wystąpił błąd podczas przetwarzania żądania: {e}", exc_info=True)
            return JsonResponse({'error': 'Wystąpił błąd serwera.'}, status=500)
    else:
        return JsonResponse({'error': 'Dozwolona jest tylko metoda POST.'}, status=405)


def naslonecznienie(request):
    years_list = list(range(2015, 2024))
    df_naslonecznienie = wczytaj_dane_naslonecznienie()
    if df_naslonecznienie is None:
        return render(request, 'app_energy25/naslonecznienie.html',
                      {'error': 'Nie udało się pobrać danych nasłonecznienia z bazy danych'})

    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/naslonecznienie.html', context)


@csrf_exempt
def pobierz_dane_naslonecznienie(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            logger.debug(f"Wybrane lata: {selected_years}")

            df_naslonecznienie = wczytaj_dane_naslonecznienie()
            logger.debug(
                f"Dane nasłonecznienia pobrane z bazy danych: {df_naslonecznienie.head().to_string() if df_naslonecznienie is not None else None}")

            if df_naslonecznienie is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych WIL z bazy danych. Sprawdź logi serwera.'},
                                    status=500)

            analiza_naslonecznienie = Naslonecznienie(df_naslonecznienie)
            dane_wykresu = analiza_naslonecznienie.pobierz_dane_dla_lat(selected_years)
            logger.debug(f"Dane wykresu po przetworzeniu: {dane_wykresu}")

            logger.info("Dane wykresu nasłonecznienia pomyślnie wygenerowane i zwrócone.")
            return JsonResponse(dane_wykresu)
        except json.JSONDecodeError as e:
            logger.error(f"Błąd dekodowania JSON: {e}", exc_info=True)
            return JsonResponse({'error': 'Nieprawidłowy format JSON.'}, status=400)
        except Exception as e:
            logger.error(f"Wystąpił błąd podczas przetwarzania żądania: {e}", exc_info=True)
            return JsonResponse({'error': 'Wystąpił błąd serwera.'}, status=500)
    else:
        return JsonResponse({'error': 'Dozwolona jest tylko metoda POST.'}, status=405)


def suma_pv(request):
    years_list = list(range(2015, 2024))
    df_suma_pv = wczytaj_dane_pv()
    if df_suma_pv is None:
        return render(request, 'app_energy25/suma_pv.html', {'error': 'Nie udało się pobrać danych PV z bazy danych'})

    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_pv.html', context)


@csrf_exempt
def pobierz_suma_pv(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_years = data.get('years', [])
            logger.debug(f"Wybrane lata: {selected_years}")

            df_suma_pv = wczytaj_dane_pv()
            logger.debug(
                f"Dane PV pobrane z bazy danych: {df_suma_pv.head().to_string() if df_suma_pv is not None else None}")

            if df_suma_pv is None:
                return JsonResponse({'error': 'Nie udało się pobrać danych PV z bazy danych. Sprawdź logi serwera.'},
                                    status=500)

            analiza_suma_pv = SumaPV(df_suma_pv)
            dane_wykresu = analiza_suma_pv.pobierz_dane_dla_lat(selected_years)
            logger.debug(f"Dane wykresu po przetworzeniu: {dane_wykresu}")

            logger.info("Dane wykresu sumy PV pomyślnie wygenerowane i zwrócone.")
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


# Zastąp tę funkcję, ponieważ będziemy bezpośrednio generować mapę w 'lokalizacje_wiatrowe'
# def generuj_widok_z_latami(request, szablon):
#     years_list = list(range(2015, 2024))
#     context = {
#         'years': years_list,
#     }
#     return render(request, f'app_energy25/{szablon}.html', context)


def suma_wiatrowa(request):
    """
    Wyświetla stronę z wyborem lat do analizy sumy produkcji wiatrowej.
    """
    years_list = list(range(2015, 2024))
    df_wil = wczytaj_dane_wil()
    if df_wil is None:
        return render(request, 'app_energy25/suma_wiatrowa.html',
                      {'error': 'Nie udało się pobrać danych WIL z bazy danych'})

    context = {
        'years': years_list,
    }
    return render(request, 'app_energy25/suma_wiatrowa.html', context)

# Usunęliśmy starą definicję lokalizacje_wiatrowe, zastępując ją nową na górze pliku.
# def lokalizacje_wiatrowe(request):
#     """
#     Wyświetla stronę z wyborem lat do analizy lokalizacji wiatrowych.
#     """
#     return generuj_widok_z_latami(request, 'lokalizacje_wiatrowe')