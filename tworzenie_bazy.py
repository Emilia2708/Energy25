import os
import pandas as pd
from sqlalchemy import create_engine

# POGODA_WIL
folder_pogoda_wil = 'C:\\Users\\HP\\Desktop\\Projekt\\pogoda\\1234'
pliki_csv_pogoda_wil = [f for f in os.listdir(folder_pogoda_wil) if f.endswith('.csv')]
nazwy_kolumn_pogoda_wil = ['Kod stacji' ,'Nazwa stacji' ,'Rok' ,'Miesiac' ,'Dzien' ,'Srednia dobowa temperatura' ,'Status pomiaru TEMP' ,'Srednia dobowa wilgotnosc wzgledna' ,'Status pomiaru WLGS' ,'Srednia dobowa predkosc wiatru' ,'Status pomiaru FWS' ,'Srednie dobowe zachmurzenie ogolne' ,'Status pomiaru NOS ' ]
df_list_pogoda_wil = []
for plik_pogoda_wil in pliki_csv_pogoda_wil:
    df_pogoda_wil = pd.read_csv(os.path.join(folder_pogoda_wil, plik_pogoda_wil)
                     , header=None
                     , encoding='cp1250'
                     , names=nazwy_kolumn_pogoda_wil
                     )
    # Parsowanie daty po wczytaniu danych
    print(f"Kolumny w df_pogoda_wil przed parsowaniem daty: {df_pogoda_wil.columns}")
    print(df_pogoda_wil.head())
    print(df_pogoda_wil[['Rok', 'Miesiac', 'Dzien']].dtypes) # Dodano
    # Konwersja na string i konkatenacja
    df_pogoda_wil['data_string'] = df_pogoda_wil['Rok'].astype(str) + '-' + df_pogoda_wil['Miesiac'].astype(str) + '-' + df_pogoda_wil['Dzien'].astype(str)
    df_pogoda_wil['data'] = pd.to_datetime(df_pogoda_wil['data_string'], format='%Y-%m-%d', errors='coerce')
    df_pogoda_wil = df_pogoda_wil.drop(['Rok', 'Miesiac', 'Dzien', 'data_string'], axis=1) # Usunięcie redundantnych kolumn
    df_list_pogoda_wil.append(df_pogoda_wil)
pogoda_wil = pd.concat(df_list_pogoda_wil, ignore_index=True)
pogoda_wil = pogoda_wil[pogoda_wil['data']<'2024-01-01']
pogoda_wil = pogoda_wil[['data', 'Kod stacji', 'Nazwa stacji', 'Srednia dobowa predkosc wiatru']]

# W P I S Y
# ImportError: lxml not found, please install or use the etree parser.
# To fix this, install the lxml library: pip install lxml
wpisy = pd.read_xml("C:\\Users\\HP\\Desktop\\Projekt\\rejestr wytwórców energii w małej instalacji.xml")
wpisy = wpisy.drop(['DKN', 'NrWpisu', 'IloscPozycji', 'IdInstalacji'], axis = 1)
wpisy['ID_obiekt'] = wpisy.reset_index().index + 1
wpisy = wpisy[wpisy['DataWpisu'] <'2024-01-01']
wpisy = wpisy[['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
             'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt']]
wpisy['Kod5'] = wpisy['Kod'].str[:5]
wpisy['Kod4'] = wpisy['Kod'].str[:4]
wpisy['Kod2'] = wpisy['Kod'].str[:2]
wpisy['Kod1'] = wpisy['Kod'].str[:1]
wpisy_pv = wpisy[wpisy['RodzajInstalacji'] == 'PVA']
wpisy_wil = wpisy[wpisy['RodzajInstalacji'] == 'WIL']

# K O D Y  P O C Z T O W E
kody_pocztowe = pd.read_csv("C:\\Users\\HP\\Desktop\\Projekt\\Kody pocztowe\\kody.csv"
                        , encoding = 'utf-8'
                        , encoding_errors = 'ignore'
                        , sep=';'
                        ,usecols= ['KOD POCZTOWY', 'MIEJSCOWOŚĆ', 'WOJEWÓDZTWO']
                        )
kody_pocztowe = kody_pocztowe.drop_duplicates()

# P O G O D A PV
folder_pogoda_pv = "C:\\Users\\HP\\Desktop\\Projekt\\pogoda\\Naslonecznienie"
pliki_csv_pogoda_pv = [f for f in os.listdir(folder_pogoda_pv) if f.endswith('.txt')]
df_list_pogoda_pv = []
for plik_pogoda_pv in pliki_csv_pogoda_pv:
    df_pogoda_pv = pd.read_csv(os.path.join(folder_pogoda_pv, plik_pogoda_pv)
             , encoding_errors = 'ignore'
             , skiprows = lambda x: x in range(21)
             , names = ['IDs', 'ID', 'Data', 'SS', 'QSS']
             )
    df_list_pogoda_pv.append(df_pogoda_pv)
pogoda_pv = pd.concat(df_list_pogoda_pv, ignore_index=True)
pogoda_pv['Data'] = pd.to_datetime(pogoda_pv['Data'], format='%Y%m%d')
pogoda_pv = pogoda_pv[pogoda_pv['Data'] <'2024-01-01']
pogoda_pv = pogoda_pv[['ID','IDs', 'Data', 'SS']]

# Dane połączenia z bazą danych PostgreSQL
db_user = 'postgres'
db_password = 'energy'
db_host = 'localhost'
db_port = '5432'
db_name = 'Energy25'

# Utworzenie URI połączenia
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

try:
    # Zapis do PostgreSQL
    pogoda_wil.to_sql('pogoda_wil', engine, if_exists='replace', index=False)
    wpisy_pv.to_sql('wpisy_pv', engine, if_exists='replace', index=False)
    wpisy_wil.to_sql('wpisy_wil', engine, if_exists='replace', index=False)
    kody_pocztowe.to_sql('kody_pocztowe', engine, if_exists='replace', index=False)
    pogoda_pv.to_sql('pogoda_pv', engine, if_exists='replace', index=False)
    print("Wszystkie DataFrames zostały zapisane do bazy danych PostgreSQL.")
except Exception as e:
    print(f"Wystąpił błąd podczas zapisu do bazy danych: {e}")
finally:
    engine.dispose()