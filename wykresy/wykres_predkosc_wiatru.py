import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PredkoscWiatru:
    """
    Klasa do analizy danych energii WIL z DataFrame.
    """
    def __init__(self, dataframe):
        """
        Inicjalizuje klasę class PredkoscWiatru z DataFrame zawierającym dane pogodowe i energii WIL.

        Args:
            dataframe (pd.DataFrame): DataFrame z kolumnami 'Data' (datetime) i 'energia' (float).
        """
        self.df = dataframe.copy()
        self.df['data'] = pd.to_datetime(self.df['data'])
        logger.debug("Inicjalizacja class PredkoscWiatru.")
        try:
            self._przetworz_daty()
            self.sredni_wiatr = self._oblicz_sredni_wiatr()
            logger.debug(f"Suma energii po obliczeniu: {self.sredni_wiatr.head().to_string() if not self.sredni_wiatr.empty else 'Pusta'}")
        except Exception as e:
            logger.error(f"Błąd podczas inicjalizacji class PredkoscWiatru: {e}", exc_info=True)
            raise

    def _przetworz_daty(self):
        """
        Konwertuje kolumnę 'Data' na typ datetime i wyodrębnia rok oraz miesiąc.
        """
        self.df['Rok'] = self.df['data'].dt.year
        self.df['Miesiąc'] = self.df['data'].dt.month
        logger.debug("Przetworzono daty, dodano kolumny 'Rok' i 'Miesiąc'.")

    def _oblicz_sredni_wiatr(self):
        """
        Oblicza sumę energii elektrycznej dla każdego miesiąca i roku.

        Returns:
            pd.Series: Seria zawierająca sumę energii z indeksami (Rok, Miesiąc).
        """
        sredni_wiatr = self.df.groupby(['Rok', 'Miesiąc'])['Srednia dobowa predkosc wiatru'].mean()
        logger.debug(f"Obliczono sumę energii. Przykładowe dane: {sredni_wiatr.head().to_string() if not sredni_wiatr.empty else 'Pusta'}")
        return sredni_wiatr

    def wyswietl_sume_energii(self):
        """
        Wyświetla obliczoną sumę energii.
        """
        print(self.sredni_wiatr)

    def pobierz_dane_dla_lat(self, wybrane_lata):
        """
        Pobiera zagregowane dane energii dla wybranych lat.

        Args:
            wybrane_lata (list): Lista lat, dla których mają zostać pobrane dane.

        Returns:
            dict: Słownik zawierający listy etykiet (Miesiąc) i wartości sum energii dla każdego roku.
        """
        dane_wykresu = {'labels': list(range(1, 13)), 'values': {}}
        logger.debug(f"Pobieranie danych dla lat: {wybrane_lata}")
        for rok in wybrane_lata:
            try:
                dane_rocznika = self.sredni_wiatr.xs(int(rok), level='Rok').to_dict()
                dane_wykresu['values'][str(rok)] = [dane_rocznika.get(miesiac, 0) for miesiac in range(1, 13)]
                logger.debug(f"Dane dla roku {rok}: {dane_wykresu['values'][str(rok)]}")
            except KeyError:
                logger.warning(f"Brak danych dla roku: {rok}")
                dane_wykresu['values'][str(rok)] = [0] * 12  # Wypełnij zerami, jeśli brak danych

        logger.debug(f"Ostateczne dane wykresu: {dane_wykresu}")
        return dane_wykresu