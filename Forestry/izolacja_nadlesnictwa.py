import geopandas as gpd

print("✂️ Projekt Portfolio #1: Filtrowanie Geometrii")
print("-" * 60)

plik_zrodlowy = "polskie_nadlesnictwa.geojson"
print(f"🗂️ Wczytuję pełną bazę kraju z pliku: {plik_zrodlowy}...")
mapa_polski = gpd.read_file(plik_zrodlowy)

# TRANSFORMACJA: Zmuszamy Pythona do wycięcia konkretnego nadleśnictwa
cel = "Daleszyce"
print(f"🔍 Szukam granic dla: Nadleśnictwo {cel}...")

# Filtrujemy tabelę, szukając dopasowania w kolumnie 'inspectorate_name'
wybrane_nadlesnictwo = mapa_polski[mapa_polski['inspectorate_name'] == cel]

if len(wybrane_nadlesnictwo) > 0:
    print(f"✅ Znaleziono geometrię dla obiektu {cel}. Odcinam resztę mapy.")
    
    plik_wyjsciowy = f"nadlesnictwo_{cel.lower()}.geojson"
    wybrane_nadlesnictwo.to_file(plik_wyjsciowy, driver="GeoJSON")
    
    print(f"💾 Gotowe! Wyizolowany obszar zapisano jako: {plik_wyjsciowy}")
else:
    print(f"❌ Nie znaleziono nadleśnictwa '{cel}' w bazie. Sprawdź wielkość liter!")
    
print("-" * 60)