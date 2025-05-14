import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Dane połączenia z bazą danych PostgreSQL
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = 'localhost'
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Utworzenie URI połączenia
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

try:
    # Pobierz dane z tabeli 'pogoda_wil'
    pogoda_wil = pd.read_sql_table('pogoda_wil', engine)

    # Pobierz dane z tabeli 'wpisy_pv'
    wpisy_pv= pd.read_sql_table('wpisy_pv', engine)

    # Pobierz dane z tabeli 'wpisy_wil'
    wpisy_wil = pd.read_sql_table('wpisy_wil', engine)

    # Pobierz dane z tabeli 'kody_pocztowe'
    kody_pocztowe = pd.read_sql_table('kody_pocztowe', engine)

    # Pobierz dane z tabeli 'pogoda_pv'
    pogoda_pv = pd.read_sql_table('pogoda_pv', engine)

except Exception as e:
    print(f"Wystąpił błąd podczas pobierania danych z bazy danych: {e}")
finally:
    engine.dispose()


pogoda_wil['Nazwa stacji'] = pogoda_wil['Nazwa stacji'].apply(lambda x: x.split('-')[0])
pogoda_wil['Kod stacji'] = pogoda_wil['Kod stacji'].astype(str)

kody_pocztowe['MIEJSCOWOŚĆ'] = kody_pocztowe['MIEJSCOWOŚĆ'].str.upper()
pogoda_wil_kody = pogoda_wil.merge(kody_pocztowe
                                   , how = 'left'
                                   ,left_on = 'Nazwa stacji'
                                   , right_on = 'MIEJSCOWOŚĆ')

pogoda_wil_kody['Kod stacji'] = pogoda_wil_kody['Kod stacji'].astype(str)
pogoda_wil_kody = pogoda_wil_kody[['Kod stacji', 'Nazwa stacji', 'KOD POCZTOWY', 'WOJEWÓDZTWO']]
pogoda_wil_kody['Kod stacji'] = pogoda_wil_kody['Kod stacji'].astype(str)

# wyciągnięcie listy stacji
lista_stacji_wil = pogoda_wil_kody.drop_duplicates(subset = ['Nazwa stacji'], keep = 'first')
lista_stacji_wil = lista_stacji_wil.dropna(subset = ['KOD POCZTOWY'])

pogoda_wil = lista_stacji_wil.merge(pogoda_wil
                             ,how = 'left'
                             ,left_on = 'Kod stacji'
                             ,right_on = 'Kod stacji')

lista_stacji_wil['KOD POCZTOWY5'] = lista_stacji_wil['KOD POCZTOWY'].str[:5]
lista_stacji_wil['KOD POCZTOWY4'] = lista_stacji_wil['KOD POCZTOWY'].str[:4]
lista_stacji_wil['KOD POCZTOWY2'] = lista_stacji_wil['KOD POCZTOWY'].str[:2]
lista_stacji_wil['KOD POCZTOWY1'] = lista_stacji_wil['KOD POCZTOWY'].str[:1]

del [pogoda_wil_kody]

### W P I S Y  W I L + P O G O D A
# połączenie elektrowni wiatrowych z pogodą

wpisy_wil_pogoda1 = wpisy_wil.merge(lista_stacji_wil
                                    , how='left'
                                    , left_on='Kod'
                                    , right_on='KOD POCZTOWY').drop_duplicates(subset=['ID_obiekt']
                                                                               , keep='first').merge(pogoda_wil
                                                                                                     , how='left'
                                                                                                     ,
                                                                                                     left_on='Kod stacji'
                                                                                                     ,
                                                                                                     right_on='Kod stacji')

brakujace1 = wpisy_wil_pogoda1[wpisy_wil_pogoda1['Kod stacji'].isna()]
wpisy_wil_pogoda1 = wpisy_wil_pogoda1.dropna(subset=['Kod stacji'])

brakujace1 = brakujace1[['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1', 'A']]

wpisy_wil_pogoda2 = brakujace1.merge(lista_stacji_wil
                                     , how='left'
                                     , left_on='Kod5'
                                     , right_on='KOD POCZTOWY5').drop_duplicates(subset=['ID_obiekt']
                                                                                 , keep='first').merge(pogoda_wil
                                                                                                       , how='left'
                                                                                                       ,
                                                                                                       left_on='Kod stacji'
                                                                                                       ,
                                                                                                       right_on='Kod stacji')

brakujace2 = wpisy_wil_pogoda2[wpisy_wil_pogoda2['Kod stacji'].isna()]
wpisy_wil_pogoda2 = wpisy_wil_pogoda2.dropna(subset=['Kod stacji'])

brakujace2 = brakujace2[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1', 'A']]

wpisy_wil_pogoda3 = brakujace2.merge(lista_stacji_wil
                                     , how='left'
                                     , left_on='Kod4'
                                     , right_on='KOD POCZTOWY4').drop_duplicates(subset=['ID_obiekt']
                                                                                 , keep='first').merge(pogoda_wil
                                                                                                       , how='left'
                                                                                                       ,
                                                                                                       left_on='Kod stacji'
                                                                                                       ,
                                                                                                       right_on='Kod stacji')

brakujace3 = wpisy_wil_pogoda3[wpisy_wil_pogoda3['Kod stacji'].isna()]
wpisy_wil_pogoda3 = wpisy_wil_pogoda3.dropna(subset=['Kod stacji'])

brakujace3 = brakujace3[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1', 'A']]

wpisy_wil_pogoda4 = brakujace3.merge(lista_stacji_wil
                                     , how='left'
                                     , left_on='Kod2'
                                     , right_on='KOD POCZTOWY2').drop_duplicates(subset=['ID_obiekt']
                                                                                 , keep='first').merge(pogoda_wil
                                                                                                       , how='left'
                                                                                                       ,
                                                                                                       left_on='Kod stacji'
                                                                                                       ,
                                                                                                       right_on='Kod stacji')

brakujace4 = wpisy_wil_pogoda4[wpisy_wil_pogoda4['Kod stacji'].isna()]
wpisy_wil_pogoda4 = wpisy_wil_pogoda4.dropna(subset=['Kod stacji'])

brakujace4 = brakujace4[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1', 'A']]

wpisy_wil_pogoda5 = brakujace4.merge(lista_stacji_wil
                                     , how='left'
                                     , left_on='Kod1'
                                     , right_on='KOD POCZTOWY1').drop_duplicates(subset=['ID_obiekt']
                                                                                 , keep='first').merge(pogoda_wil
                                                                                                       , how='left'
                                                                                                       ,
                                                                                                       left_on='Kod stacji'
                                                                                                       ,
                                                                                                       right_on='Kod stacji')

brakujace5 = wpisy_wil_pogoda5[wpisy_wil_pogoda5['Kod stacji'].isna()]
wpisy_wil_pogoda5 = wpisy_wil_pogoda5.dropna(subset=['Kod stacji'])

wpisy_wil_pogoda = pd.concat(
    [wpisy_wil_pogoda1, wpisy_wil_pogoda2, wpisy_wil_pogoda3, wpisy_wil_pogoda4, wpisy_wil_pogoda5], ignore_index=True)

wpisy_wil_pogoda = wpisy_wil_pogoda[wpisy_wil_pogoda['DataWpisu'] < wpisy_wil_pogoda['data']]

wpisy_wil_pogoda = wpisy_wil_pogoda[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'A', 'Kod stacji', 'Nazwa stacji', 'data',
     'Srednia dobowa predkosc wiatru']]

wpisy_wil_pogoda['Energia'] = (0.5 * 1.22 * wpisy_wil_pogoda['A'] * (
            wpisy_wil_pogoda['Srednia dobowa predkosc wiatru'] ** 3) * 0.95 * 0.85 * 0.7 * 24) / 1000

del [wpisy_wil_pogoda1, wpisy_wil_pogoda2, wpisy_wil_pogoda3, wpisy_wil_pogoda4, wpisy_wil_pogoda5, brakujace1,
     brakujace2, brakujace3, brakujace4, brakujace5]

### P O G O D A  P V   K O D Y
# Połączenie tabeli pogoda pv z kodami pocztowymi

from unidecode import unidecode

pogoda_pv['Data'] = pd.to_datetime(pogoda_pv['Data'], format='%Y%m%d')
# pozostawiamy tylko dane pogodowe po 01.01.2015 roku
pogoda_pv = pogoda_pv[pogoda_pv['Data'] >= '2015-01-01']
# zamieniamy braki danych srednią wartoscią zasłonecznienia z danego dnia
pogoda_pv7 = pogoda_pv[pogoda_pv['SS'] != -9999].groupby('Data')['SS'].mean()
pogoda_pv.loc[pogoda_pv['SS'] == -9999, 'SS'] = pogoda_pv[pogoda_pv['SS'] == -9999]['Data'].map(pogoda_pv7)
stacje_pv = pd.read_excel("C:\\Users\\HP\\Desktop\\Projekt\\pogoda\\stacje.xlsx"
                          , dtype={'nazwa': str})
stacje_pv['nazwa'] = stacje_pv['nazwa'].str.rstrip()
kody_pocztowe_bez_pl = kody_pocztowe
# usuwamy polskie znaki z nazw miejscowosci
kody_pocztowe_bez_pl['MIEJSCOWOŚĆ'] = kody_pocztowe_bez_pl['MIEJSCOWOŚĆ'].apply(unidecode)
stacje_pv_kody = stacje_pv.merge(kody_pocztowe
                                 , how='left'
                                 , left_on='nazwa'
                                 , right_on='MIEJSCOWOŚĆ')

stacje_pv_kody = stacje_pv_kody.drop_duplicates(subset=['numer2'], keep='first')
stacje_pv_kody2 = stacje_pv_kody[stacje_pv_kody['MIEJSCOWOŚĆ'].isna()]
stacje_pv_kody2['nazwa'] = stacje_pv_kody2['nazwa'].apply(lambda x: x.split('-')[0])
stacje_pv2 = stacje_pv_kody2[['numer1', 'numer2', 'nazwa', 'Unnamed: 3', 'dlugosc', 'szerokosc']]
stacje_pv_kody3 = stacje_pv2.merge(kody_pocztowe
                                   , how='left'
                                   , left_on='nazwa'
                                   , right_on='MIEJSCOWOŚĆ')
stacje_pv_kody3 = stacje_pv_kody3.drop_duplicates(subset=['numer2'], keep='first')
stacje_pv_kody3 = stacje_pv_kody3.dropna(subset=['MIEJSCOWOŚĆ'])
stacje_pv_kody = stacje_pv_kody.dropna(subset=['MIEJSCOWOŚĆ'])
stacje_pv_kody = pd.concat([stacje_pv_kody, stacje_pv_kody3])
stacje_pv_kody = stacje_pv_kody[['numer1', 'nazwa', 'dlugosc', 'szerokosc', 'KOD POCZTOWY',
                                 'WOJEWÓDZTWO']]

stacje_pv_kody['KOD POCZTOWY5'] = stacje_pv_kody['KOD POCZTOWY'].str[:5]
stacje_pv_kody['KOD POCZTOWY4'] = stacje_pv_kody['KOD POCZTOWY'].str[:4]
stacje_pv_kody['KOD POCZTOWY2'] = stacje_pv_kody['KOD POCZTOWY'].str[:2]
stacje_pv_kody['KOD POCZTOWY1'] = stacje_pv_kody['KOD POCZTOWY'].str[:1]

pogoda_pv['ID'] = pogoda_pv['ID'].astype(str)

del [pogoda_pv7, stacje_pv, stacje_pv2, stacje_pv_kody2, stacje_pv_kody3]

### W P I S Y  P V + P O G O D A
# Połączenie elektrowni fotowoltaicznych z informacjami o nasłonecznieniu

wpisy_pv_pogoda1 = wpisy_pv.merge(stacje_pv_kody
                                  , how='left'
                                  , left_on='Kod'
                                  , right_on='KOD POCZTOWY').drop_duplicates(subset=['ID_obiekt']
                                                                             , keep='first').merge(pogoda_pv
                                                                                                   , how='left'
                                                                                                   , left_on='numer1'
                                                                                                   , right_on='IDs')

brakujace1 = wpisy_pv_pogoda1[wpisy_pv_pogoda1['numer1'].isna()]
wpisy_pv_pogoda1 = wpisy_pv_pogoda1.dropna(subset=['numer1'])

brakujace1 = brakujace1[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1']]

wpisy_pv_pogoda2 = brakujace1.merge(stacje_pv_kody
                                    , how='left'
                                    , left_on='Kod5'
                                    , right_on='KOD POCZTOWY5').drop_duplicates(subset=['ID_obiekt']
                                                                                , keep='first').merge(pogoda_pv
                                                                                                      , how='left'
                                                                                                      , left_on='numer1'
                                                                                                      , right_on='IDs')

brakujace2 = wpisy_pv_pogoda2[wpisy_pv_pogoda2['numer1'].isna()]
wpisy_pv_pogoda2 = wpisy_pv_pogoda2.dropna(subset=['numer1'])

brakujace2 = brakujace2[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1']]

wpisy_pv_pogoda3 = brakujace2.merge(stacje_pv_kody
                                    , how='left'
                                    , left_on='Kod4'
                                    , right_on='KOD POCZTOWY4').drop_duplicates(subset=['ID_obiekt']
                                                                                , keep='first').merge(pogoda_pv
                                                                                                      , how='left'
                                                                                                      , left_on='numer1'
                                                                                                      , right_on='IDs')

brakujace3 = wpisy_pv_pogoda3[wpisy_pv_pogoda3['numer1'].isna()]
wpisy_pv_pogoda3 = wpisy_pv_pogoda3.dropna(subset=['numer1'])

brakujace3 = brakujace3[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1']]

wpisy_pv_pogoda4 = brakujace3.merge(stacje_pv_kody
                                    , how='left'
                                    , left_on='Kod2'
                                    , right_on='KOD POCZTOWY2').drop_duplicates(subset=['ID_obiekt']
                                                                                , keep='first').merge(pogoda_pv
                                                                                                      , how='left'
                                                                                                      , left_on='numer1'
                                                                                                      , right_on='IDs')

brakujace4 = wpisy_pv_pogoda4[wpisy_pv_pogoda4['numer1'].isna()]
wpisy_pv_pogoda4 = wpisy_pv_pogoda4.dropna(subset=['numer1'])

brakujace4 = brakujace4[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'Kod5', 'Kod4', 'Kod2', 'Kod1']]

wpisy_pv_pogoda5 = brakujace4.merge(stacje_pv_kody
                                    , how='left'
                                    , left_on='Kod1'
                                    , right_on='KOD POCZTOWY1').drop_duplicates(subset=['ID_obiekt']
                                                                                , keep='first').merge(pogoda_pv
                                                                                                      , how='left'
                                                                                                      , left_on='numer1'
                                                                                                      , right_on='IDs')

brakujace5 = wpisy_pv_pogoda5[wpisy_pv_pogoda5['numer1'].isna()]
wpisy_pv_pogoda5 = wpisy_pv_pogoda5.dropna(subset=['numer1'])

wpisy_pv_pogoda = pd.concat([wpisy_pv_pogoda1, wpisy_pv_pogoda2, wpisy_pv_pogoda3, wpisy_pv_pogoda4, wpisy_pv_pogoda5],
                            ignore_index=True)

wpisy_pv_pogoda = wpisy_pv_pogoda[wpisy_pv_pogoda['DataWpisu'] < wpisy_pv_pogoda['Data']]

wpisy_pv_pogoda = wpisy_pv_pogoda[
    ['Nazwa', 'NIP', 'Kod', 'Miejscowosc', 'Wojewodztwo', 'DataWpisu', 'MiejscowoscInstalacji', 'WojewodztwoInstalacji',
     'RodzajInstalacji', 'MocEEInstalacji', 'ID_obiekt', 'numer1', 'nazwa', 'dlugosc', 'szerokosc', 'Data', 'SS']]

wpisy_pv_pogoda['energia'] = (wpisy_pv_pogoda['SS'] * wpisy_pv_pogoda['MocEEInstalacji'] * 1000 * 70) / 1000

del [brakujace1, brakujace2, brakujace3, brakujace4, brakujace5, wpisy_pv_pogoda1, wpisy_pv_pogoda2, wpisy_pv_pogoda3,
     wpisy_pv_pogoda4, wpisy_pv_pogoda5]

# Dane połączenia z bazą danych PostgreSQL
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASS')
db_host = 'localhost'
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Utworzenie URI połączenia
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

try:
    # Zapis do PostgreSQL
    wpisy_wil_pogoda.to_sql('wpisy_wil_pogoda', engine, if_exists='replace', index=False)
    wpisy_pv_pogoda.to_sql('wpisy_pv_pogoda', engine, if_exists='replace', index=False)
    print("Wszystkie DataFrames zostały zapisane do bazy danych PostgreSQL.")
except Exception as e:
    print(f"Wystąpił błąd podczas zapisu do bazy danych: {e}")
finally:
    engine.dispose()
