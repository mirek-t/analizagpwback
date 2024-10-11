import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import pandas as pd
from datetime import datetime

#Czas trwania skryptu
start_time = time.time()

#Pobranie dzisiejszej daty
dzisiaj = datetime.now()
sformatowana_data = dzisiaj.strftime("%d%m%Y")

#Zmienne początkowe
href_do_url = []
counter_href_do_url = 0
delay = random.uniform(1, 3)

# Utwórz dane do pracy w pandas na excelu
data = {
    'Nazwa Spółki': [],
    'ISIN': [],
    'Kurs PLN': [],
    'Zmiana w procentach': [],
    'Kurs Otwarcia': [],
    'Minimum': [],
    'Maksimum': [],
    'Obrót (szt)': [],
    'Obrót (PLN)': [],
    'Data aktualizacji': [],
    'Cena/Zysk (C/Z)': [],
    'Cena/War. Księg. (C/WK)': [],
    'Cena/Przychody (C/P)': [],
    'Wartość księgowa (mln.)': [],
    'Kapitalizacja (mln.)': [],
    'Liczba akcji (mln.)': [],
    'Free float (%)': [],
    'ROA': [],
    'ROE': [],
    'ROS': [],
    'Zadłużenie ogółem (%)': [],
    'Zadłużenie krótkoterminowe (%)': [],
    'Zadłużenie długoterminowe (%)': [],
    'Data sprawozdania': [],
}

# URL do pobrania
# url = "https://www.gpw.pl/spolki"
url = "https://www.money.pl/gielda/spolki-gpw/"

# Wysłanie żądania GET do strony
response = requests.get(url)
time.sleep(delay)

# Sprawdzenie, czy żądanie zakończyło się sukcesem
if response.status_code == 200:
    # Parsowanie HTML za pomocą BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Znalezienie elementu
    lista_spolek = soup.find_all('div', attrs={"class": "rt-tr -odd"})
    # print(lista_spolek)

    if lista_spolek: #lista
        #Czyszczenie pliku
        with open(f'gpw_lista_spolek_{sformatowana_data}.txt', 'w', encoding='utf-8') as plik:
            pass
        
        #Przetwarzanie danych spółek
        for spolka_z_listy in lista_spolek:
            #Pobranie nazwy spółki
            nazwa_spolki = spolka_z_listy.select('div')[0]
            #Dodawanie nazwy do listy obiektu data
            data['Nazwa Spółki'].append(nazwa_spolki.text.strip())
        
            #Pobranie ISIN
            link = spolka_z_listy.find('a', attrs={"class": "sc-18yizqs-0 sUail"})
            href = link.get('href')
            cut_before_bslash = href.rsplit('/', 1)[-1]
            isin = cut_before_bslash.split('.')[0]
            href_do_url.append(isin)
            #Dodawanie ISIN do obiektu data
            data['ISIN'].append(isin)
                        
            #Pobranie kursu spółki i dodanie go do obiektu data
            kurs_PLN = spolka_z_listy.select('div')[2]
            kurs_PLN_formated = kurs_PLN.text.replace(",", ".").replace("\xa0", "")
            if kurs_PLN_formated != "—":
                data['Kurs PLN'].append(float(kurs_PLN_formated))
            else:
                data['Kurs PLN'].append(None)
                
            #Zmiana w procentach, dodanie wartości do obiektu data
            zmiana_procentowo = spolka_z_listy.select('div')[4]
            zmiana_procentowo_formated = zmiana_procentowo.text.replace(",", ".").replace("\xa0", "")
            if zmiana_procentowo_formated != "—":
                data['Zmiana w procentach'].append(float(zmiana_procentowo_formated))
            else:
                data['Zmiana w procentach'].append(None)
                
            #Otwarcie i dodanie danej do obiektu data
            otwarcie = spolka_z_listy.select('div')[6]
            otwarcie_formated = otwarcie.text.replace(",", ".").replace("\xa0", "")
            if otwarcie_formated != "—":   
                data['Kurs Otwarcia'].append(float(otwarcie_formated))
            else:
                data['Kurs Otwarcia'].append(None)
                        
            #Minimum i dodanie danej do obiektu data
            minimum = spolka_z_listy.select('div')[8]     
            minimum_formated = minimum.text.replace(",", ".").replace("\xa0", "")
            if minimum_formated != "—":   
                data['Minimum'].append(float(minimum_formated))
            else:
                data['Minimum'].append(None)
                        
            #Maksimum i dodanie danej do obiektu data
            maksimum = spolka_z_listy.select('div')[10]      
            maksimum_formated = maksimum.text.replace(",", ".").replace("\xa0", "")  
            if maksimum_formated != "—":  
                data['Maksimum'].append(float(maksimum_formated))
            else:
                data['Maksimum'].append(None)
            
            #Obrót (szt) i dodanie danej do obiektu data
            obrot_szt = spolka_z_listy.select('div')[12]   
            obrot_szt_formated = obrot_szt.text.replace(",", ".").replace("\xa0", "")         
            if obrot_szt_formated != "—":
                data['Obrót (szt)'].append(float(obrot_szt_formated))
            else:    
                data['Obrót (szt)'].append(None)
            
            #Obrót (PLN) i dodanie danej do obiektu data
            obrot_PLN = spolka_z_listy.select('div')[14]
            obrot_PLN_formated = obrot_PLN.text.replace(",", ".").replace("\xa0", "")
            if obrot_PLN_formated != "—":
                data["Obrót (PLN)"].append(float(obrot_PLN_formated))
            else:    
                data["Obrót (PLN)"].append(None)
            
            #Data aktualizacji i dodanie danej do obiektu data
            data_aktualizacji = spolka_z_listy.select('div')[16]
            data['Data aktualizacji'].append(data_aktualizacji.text.replace(",", "."))
            
            #Pobieranie wskaźników poszczególnych spółek
            url_spolki = url+href_do_url[counter_href_do_url]+".html"
            
            # Wysłanie żądania GET do strony
            response = requests.get(url_spolki)
            time.sleep(delay)
            
            # Sprawdzenie, czy żądanie zakończyło się sukcesem
            if response.status_code == 200:
                
                # Parsowanie HTML za pomocą BeautifulSoup
                soup2 = BeautifulSoup(response.text, 'html.parser')
                
                # Znalezienie elementu
                wskazniki = soup2.find('dl', attrs={"class": "wi06td-4 cKAzcw"})

                if wskazniki: #lista
            
                    c_z = wskazniki.select('dd')[0]
                    c_z_formated = c_z.text.replace(",", ".").replace("\xa0", "")
                    if c_z_formated != "—":
                        data['Cena/Zysk (C/Z)'].append(float(c_z_formated))
                    else:
                        data['Cena/Zysk (C/Z)'].append(None)
                    
                    c_wk = wskazniki.select('dd')[1]
                    c_wk_formated = c_wk.text.replace(",", ".").replace("\xa0", "")
                    if c_wk_formated != "—":
                        data["Cena/War. Księg. (C/WK)"].append(float(c_wk_formated))
                    else:
                        data["Cena/War. Księg. (C/WK)"].append(None)
                    
                    
                    c_p = wskazniki.select('dd')[2]
                    c_p_formated = c_p.text.replace(",", ".").replace("\xa0", "")
                    if c_p_formated != "—":
                        data["Cena/Przychody (C/P)"].append(float(c_p_formated))
                    else:
                        data["Cena/Przychody (C/P)"].append(None)
                    
                    
                    war_ks = wskazniki.select('dd')[3]
                    war_ks_formated = war_ks.text.replace(",", ".").replace("\xa0", "")
                    if war_ks_formated != "—":
                        data["Wartość księgowa (mln.)"].append(float(war_ks_formated))
                    else:
                        data["Wartość księgowa (mln.)"].append(None)
                        
                    kapitalizacja = wskazniki.select('dd')[4]
                    kapitalizacja_formated = kapitalizacja.text.replace(",", ".").replace("\xa0", "")
                    if kapitalizacja_formated != "—":
                        data["Kapitalizacja (mln.)"].append(float(kapitalizacja_formated))
                    else:
                        data["Kapitalizacja (mln.)"].append(None)
                                            
                        
                    liczba_akcji = wskazniki.select('dd')[5]
                    liczba_akcji_formeted = liczba_akcji.text.replace(",", ".").replace("\xa0", "")
                    if liczba_akcji_formeted != "—":
                        data["Liczba akcji (mln.)"].append(float(liczba_akcji_formeted))
                    else:
                        data["Liczba akcji (mln.)"].append(None)
                    
                    
                    free_float = wskazniki.select('dd')[6]
                    free_float_formated = free_float.text.replace(",", ".").replace("\xa0", "")
                    if free_float_formated != "—":
                        data["Free float (%)"].append(float(free_float_formated))
                    else:
                        data["Free float (%)"].append(None)
                        
                    
                    roa = wskazniki.select('dd')[7]
                    roa_formated = roa.text.replace(",", ".").replace("\xa0", "")
                    if roa_formated != "—":
                        data["ROA"].append(float(roa_formated))
                    else:
                        data["ROA"].append(None)
                    
                    
                    roe = wskazniki.select('dd')[8]
                    roe_formated = roe.text.replace(",", ".").replace("\xa0", "")
                    if roe_formated != "—":
                        data["ROE"].append(float(roe_formated))
                    else:
                        data["ROE"].append(None)
                    
                    
                    ros = wskazniki.select('dd')[9]
                    ros_formated = ros.text.replace(",", ".").replace("\xa0", "")
                    if ros_formated != "—":
                        data["ROS"].append(float(ros_formated))
                    else:
                        data["ROS"].append(None)
                    
                    
                    zadluzenie_ogolem = wskazniki.select('dd')[10]
                    zadluzenie_ogolem_formated = zadluzenie_ogolem.text.replace(",", ".").replace("\xa0", "")
                    if zadluzenie_ogolem_formated != "—":
                        data["Zadłużenie ogółem (%)"].append(float(zadluzenie_ogolem_formated))
                    else:    
                        data["Zadłużenie ogółem (%)"].append(None)  # Można dodać None, jeśli dane są puste
                    
                    
                    zadluzenie_krotkoterminowe = wskazniki.select('dd')[11]
                    zadluzenie_krotkoterminowe_formated = zadluzenie_krotkoterminowe.text.replace(",", ".").replace("\xa0", "")
                    if zadluzenie_krotkoterminowe_formated != "—": 
                        data["Zadłużenie krótkoterminowe (%)"].append(float(zadluzenie_krotkoterminowe_formated))
                    else:
                        data["Zadłużenie krótkoterminowe (%)"].append(None)
                        
                        
                    zadluzenie_dlugoterminowe = wskazniki.select('dd')[12]
                    zadluzenie_dlugoterminowe_formated = zadluzenie_dlugoterminowe.text.replace(",", ".").replace("\xa0", "")
                    if zadluzenie_dlugoterminowe_formated != "—": 
                        data["Zadłużenie długoterminowe (%)"].append(float(zadluzenie_dlugoterminowe_formated))
                    else:
                        data["Zadłużenie długoterminowe (%)"].append(None)
                        
                        
                    data_sprawozdania = wskazniki.select('dd')[13]
                    data["Data sprawozdania"].append(data_sprawozdania.text.replace(",", "."))
                    
                    #Podbicie licznika
                    counter_href_do_url = counter_href_do_url + 1
                    print(f"Zapisuję {nazwa_spolki.text.strip()} do pliku.")
                    
                    # Zapisywanie wyników do pliku
                    with open(f'gpw_lista_spolek_{sformatowana_data}.txt', 'a', encoding='utf-8') as plik:
                        plik.write(nazwa_spolki.text.strip()+'; '+isin+'; '+kurs_PLN.text+'; '+zmiana_procentowo.text+'; '+otwarcie.text+'; '+minimum.text+'; '+maksimum.text+'; '+obrot_szt.text+'; '+obrot_PLN.text+'; '+data_aktualizacji.text+'; '+c_z.text+'; '+c_wk.text+'; '+c_p.text+'; '+war_ks.text+'; '+kapitalizacja.text+'; '+liczba_akcji.text+'; '+free_float.text+'; '+roa.text+'; '+roe.text+'; '+ros.text+'; '+zadluzenie_ogolem.text+'; '+zadluzenie_krotkoterminowe.text+'; '+zadluzenie_dlugoterminowe.text+'; '+data_sprawozdania.text+'; '+'\n')
                
                else:
                    print("Brak danych o wskaznikach.")
            else:
                print(f"Błąd w ładowaniu podstrony spółki: {response.status_code}")
    else:
        print("Pusta lista bądź jej brak.")
else:
    print(f"Błąd w ładowaniu strony: {response.status_code}")


# Odczytaj dane z pliku
with open(f'gpw_lista_spolek_{sformatowana_data}.txt', 'r', encoding='utf-8') as plik:
    zawartosc = plik.read()
    print(zawartosc)

end_time = time.time()  # Zapisanie czasu końcowego
execution_time = end_time - start_time  # Obliczenie czasu trwania
print(f"Czas wykonania: {execution_time} sekund")

#Praca w pandas i procesowanie danych
df = pd.DataFrame(data)

# Zapisz do pliku Excel
df.to_excel(f'gpw_lista_spolek_{sformatowana_data}.xlsx', index=False, sheet_name='Wskazniki')

# Odczytaj plik Excel
dd = pd.read_excel(f'gpw_lista_spolek_{sformatowana_data}.xlsx', sheet_name=0)  # Możesz również użyć nazwyu arkusza, np. sheet_name='Wskazniki'

# Wyświetl pierwsze pięć wierszy
print(dd.head())