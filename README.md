# Projekt portal ENERGY25  
1. Klonowanie projektu

```sh
git clone https://github.com/Emilia2708/Energy25.git
```

2. Tworzenie wirtualnej zmiennej środowiskowej
```shell
python -m venv .venv
```

3. Aktywacja zmiennej środowiskowej
```shell
.venv/Scripts/activate
```

4. Instalacja pakietów / paczek
```shell
pip install -r requirements.txt
```

5. Stworzenie / podłączenie bazy danych postgresql
   - stworzenie pliku .env
   - skopiowanie zawartości z pliku .env.example
   - wklejenie zawartości do pliku .env
   - uzupełnienie o dane lokalne (Twoje dane konfiguracyjne)