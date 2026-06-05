import geopandas as gpd

print("✂️ Moduł Transformacji: Filtrowanie danych przestrzennych...")
print("-" * 60)

plik_wejsciowy = "surowe_dane_z_sieci.geojson"
tabela_swiat = gpd.read_file(plik_wejsciowy)

print(f"🌍 Wczytano mapę świata. Liczba wszystkich państw (wierszy): {len(tabela_swiat)}")
print("-" * 60)

# DEBUGGOWANIE: Zobaczmy, jakie dokładnie kolumny pobraliśmy z internetu!
print("🔍 Skanowanie struktury bazy danych. Dostępne kolumny to:")
# Ta linijka wypluje nam listę wszystkich 64 nazw kolumn z tej tabeli
print(list(tabela_swiat.columns))
print("-" * 60)

# TRANSFORMACJA
# Zamiast 'ADMIN', używamy kolumny 'name', która jest standardem w tej konkretnej bazie danych
polska_geometria = tabela_swiat[tabela_swiat["name"] == "Poland"]

if len(polska_geometria) > 0:
    print("✅ Znaleziono Polskę! Odcinam resztę świata...")
    
    plik_wyjsciowy = "polska_granica.geojson"
    polska_geometria.to_file(plik_wyjsciowy, driver="GeoJSON")
    
    print(f"💾 Nowy, lekki plik mapowy zapisany jako: {plik_wyjsciowy}")
else:
    print("❌ Nadal nie znaleziono Polski. Spójrz na wygenerowaną listę kolumn wyżej i poszukaj odpowiedniej nazwy!")
    
print("-" * 60)