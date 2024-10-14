import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import pandas as pd
from datetime import datetime
import json

#Czas trwania skryptu
start_time = time.time()

#Pobranie dzisiejszej daty
dzisiaj = datetime.now()
sformatowana_data = dzisiaj.strftime("%d%m%Y")

#Zmienne początkowe
delay = random.uniform(1, 3)

# Utwórz dane do pracy w pandas na excelu
data = {
    'Nazwa Spółki': [],
    'href': [],
    'ISIN': [],
    'EKD': [],
}

# URL do pobrania
url = "https://www.bankier.pl"
url_WIGdiv = "/inwestowanie/profile/quote.html?symbol=WIGDIV"

# Wysłanie żądania GET do strony
response = requests.get(f'{url}{url_WIGdiv}')
time.sleep(delay)

# Sprawdzenie, czy żądanie zakończyło się sukcesem
if response.status_code == 200:
    # Parsowanie HTML za pomocą BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Znalezienie elementu
    lista_spolek_dywidendowych = soup.find_all('td', attrs={"class": "colWalor textNowrap"})

    if lista_spolek_dywidendowych: #lista
        #Czyszczenie pliku
        with open(f'WIGdiv_{sformatowana_data}.txt', 'w', encoding='utf-8') as plik:
            pass
    
        #Przetwarzanie danych spółek
        for td in lista_spolek_dywidendowych:
            company_name = td.get_text(strip=True)  # Wydobywa tekst, usuwając białe znaki
            link = td.find('a')['href']  # Znajduje tag <a> i wydobywa atrybut href
            
            #Dodawanie nazwy do listy obiektu data
            data['Nazwa Spółki'].append(company_name)
            data['href'].append(link)

                        
    else:
        print("Pusta lista bądź jej brak.")
else:
    print(f"Błąd w ładowaniu strony: {response.status_code}")

for nazwa_spolki in data['Nazwa Spółki']:
    # Wysłanie żądania GET do strony
    response = requests.get(f'https://www.bankier.pl/gielda/notowania/akcje/{nazwa_spolki}/podstawowe-dane')
    time.sleep(delay)
    
    # Sprawdzenie, czy żądanie zakończyło się sukcesem
    if response.status_code == 200:
        # Parsowanie HTML za pomocą BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
      
        # Wydobycie wartości ISIN
        isin_value = None
        ekd = None
        # Wyszukiwanie wszystkich tabel w HTML
        tables = soup.find_all('table')
        
        # Iteracja przez wszystkie tabele w celu znalezienia ISIN
        for table in tables:
            # Szukamy wierszy tabeli
            rows = table.find_all('tr')
            for row in rows:
                # Sprawdzamy, czy komórka z tekstem zawiera 'ISIN'
                if 'ISIN' in row.get_text():
                    # Wydobywamy wartość ISIN z drugiej komórki w tym wierszu
                    isin_value = row.find_all('td')[1].get_text(strip=True)
                    break
            if isin_value:  # Jeśli znaleziono ISIN, przerywamy dalsze przeszukiwanie
                break
        
        # Iteracja przez wszystkie tabele w celu znalezienia EKD
        for table in tables:
            # Szukamy wierszy tabeli
            rows = table.find_all('tr')
            for row in rows:
                # Sprawdzamy, czy komórka z tekstem zawiera 'EKD'
                if 'EKD' in row.get_text():
                    # Wydobywamy wartość ISIN z drugiej komórki w tym wierszu
                    ekd = row.find_all('td')[1].get_text(strip=True)
                    break
            if ekd:  # Jeśli znaleziono ISIN, przerywamy dalsze przeszukiwanie
                break


        
    else:
        print(f"Błąd w ładowaniu strony: {response.status_code}")

# Zapisanie wartości ISIN do obiektu
data["ISIN"].append(isin_value)
data["EKD"].append(ekd)

# Konwersja obiektu Python do formatu JSON
json_data = json.dumps(data, indent=4)  # indent=4 sprawia, że JSON jest sformatowany w czytelny sposób

# Zapisywanie wyników do pliku
with open(f'WIGdiv_{sformatowana_data}.txt', 'a', encoding='utf-8') as plik:
    plik.write(json_data)

# Odczytaj dane z pliku
with open(f'WIGdiv_{sformatowana_data}.txt', 'r', encoding='utf-8') as plik:
    zawartosc = plik.read()
    print(zawartosc)

end_time = time.time()  # Zapisanie czasu końcowego
execution_time = end_time - start_time  # Obliczenie czasu trwania
print(f"Czas wykonania: {execution_time} sekund")