import pandas as pd
import plotly.graph_objects as go

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

    def generuj_wykres_energii(self, wybrane_lata=None, tytul='Energia w elektrowniach słonecznych', os_x_tytul='Miesiąc', os_y_tytul='Suma energii (MWh)'):
        """
        Generuje interaktywny wykres liniowy przedstawiający sumę energii dla wybranych lat.

        Args:
            wybrane_lata (list, optional): Lista lat, dla których ma zostać wygenerowany wykres.
                                          Jeśli None, wyświetlone zostaną wszystkie dostępne lata. Domyślnie None.
            tytul (str, optional): Tytuł wykresu. Domyślnie 'Energia w elektrowniach słonecznych'.
            os_x_tytul (str, optional): Tytuł osi X. Domyślnie 'Miesiąc'.
            os_y_tytul (str, optional): Tytuł osi Y. Domyślnie 'Suma energii (MWh)'.

        Returns:
            plotly.graph_objects.Figure: Obiekt figury Plotly.
        """
        fig_pv = go.Figure()
        for rok, grupa in self.suma_energii.groupby(level=0):
            if wybrane_lata is None or rok in wybrane_lata:
                fig_pv.add_trace(go.Scatter(x=grupa.index.get_level_values(1), y=grupa.values, mode='lines', name=str(rok)))

        fig_pv.update_layout(title=tytul,
                             xaxis_title=os_x_tytul,
                             yaxis_title=os_y_tytul)
        return fig_pv

# Przykład użycia klasy z wyborem lat:
# Załóżmy, że masz DataFrame o nazwie 'wpisy_pv_pogoda'
analiza = AnalizaEnergiiPV(wpisy_pv_pogoda)

# Wyświetl sumę energii (opcjonalnie)
analiza.wyswietl_sume_energii()

# Wygeneruj wykres dla wszystkich lat
wykres_wszystkie = analiza.generuj_wykres_energii()
wykres_wszystkie.show()

# Wygeneruj wykres tylko dla wybranych lat (np. 2022 i 2023)
wybrane_lata_do_wykresu = [2022, 2023]
wykres_wybrane = analiza.generuj_wykres_energii(wybrane_lata=wybrane_lata_do_wykresu)
wykres_wybrane.show()

# Wygeneruj wykres z niestandardowym tytułem
wykres_niestandardowy = analiza.generuj_wykres_energii(wybrane_lata=[2024], tytul='Energia PV w 2024 roku')
wykres_niestandardowy.show()