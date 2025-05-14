import pandas as pd

class AnalizaEnergiiPV:
    def __init__(self, dataframe):
        """
        Inicjalizuje klasę AnalizaEnergiiPV z DataFrame zawierającym dane pogodowe i energii PV.

        Args:
            dataframe (pd.DataFrame): DataFrame z kolumnami 'Data' (datetime) i 'energia' (float).
        """
        self.df = dataframe.copy()
        self._przetworz_daty()
        self.suma_energii = self._oblicz_sume_energii()

    def _przetworz_daty(self):
        """
        Konwertuje kolumnę 'Data' na typ datetime i wyodrębnia rok oraz miesiąc.
        """
        self.df['Data'] = pd.to_datetime(self.df['Data'])
        self.df['Rok'] = self.df['Data'].dt.year
        self.df['Miesiąc'] = self.df['Data'].dt.month

    def _oblicz_sume_energii(self):
        """
        Oblicza sumę energii elektrycznej dla każdego miesiąca i roku.

        Returns:
            pd.Series: Seria zawierająca sumę energii z indeksami (Rok, Miesiąc).
        """
        return self.df.groupby(['Rok', 'Miesiąc'])['energia'].sum()

    def wyswietl_sume_energii(self):
        """
        Wyświetla obliczoną sumę energii.
        """
        print(self.suma_energii)

    def pobierz_dane_dla_lat(self, wybrane_lata):
        """
        Pobiera zagregowane dane energii dla wybranych lat w formacie odpowiednim dla Chart.js.

        Args:
            wybrane_lata (list): Lista lat, dla których mają zostać pobrane dane.

        Returns:
            dict: Słownik zawierający listy etykiet (Rok - Miesiąc) i wartości sum energii.
        """
        dane_wykresu = {'labels': [], 'values': []}
        for (rok, miesiac), energia in self.suma_energii.items():
            if rok in wybrane_lata:
                dane_wykresu['labels'].append(f'{rok} - {miesiac:02d}')
                dane_wykresu['values'].append(energia)
        return dane_wykresu