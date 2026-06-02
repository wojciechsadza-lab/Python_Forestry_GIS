import geopandas as gpd
import pandas as pd

print("🧮 Projekt Portfolio #1: Automatyczny Raport Taksacyjny")
print("-" * 60)

# 1. Wczytujemy naszą próbkę wydzieleń leśnych z dysku
plik_wejsciowy = "probka_wydzielen.geojson"
tabela = gpd.read_file(plik_wejsciowy)

# 2. CZYSZCZENIE DANYCH (Data Cleaning)
# W prawdziwym świecie dane często mają puste luki (tzw. Null/NaN). 
# Zamieniamy puste miejsca w kolumnie funkcji lasu na tekst "Brak kategorii", żeby kod się nie wywrócił.
tabela['forest_fun'] = tabela['forest_fun'].fillna("Brak kategorii")

# Przed obliczeniami upewniamy się, że powierzchnia to na pewno liczba
tabela['sub_area'] = pd.to_numeric(tabela['sub_area'], errors='coerce')

# 3. ZAAWANSOWANA MATEMATYKA (Grupowanie)
# Grupujemy wydzielenia według funkcji lasu ('forest_fun') i sumujemy ich powierzchnię ('sub_area').
# Funkcja .round(2) zaokrągla wyniki do dwóch miejsc po przecinku.
raport = tabela.groupby('forest_fun')['sub_area'].sum().round(2)

print("📊 Suma powierzchni (ha) wydzieleń leśnych z podziałem na ich funkcję:")
print(raport)
print("-" * 60)

# 4. BONUS: Znajdujemy największe pojedyncze wydzielenie w pobranej paczce
najwieksze = tabela.loc[tabela['sub_area'].idxmax()]
print(f"🌲 Największe fizyczne wydzielenie w tej próbce ma powierzchnię: {najwieksze['sub_area']} ha.")
print("   Oto pełna karta informacyjna tego wydzielenia:")
# Wypisujemy absolutnie wszystkie dane, które serwer przypiął do tego kawałka lasu
print(najwieksze)
print("-" * 60)