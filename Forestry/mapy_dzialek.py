import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

print("🌍 Moduł GIS: Generowanie mapy leśnej...")
print("-" * 50)

# 1. Nasze dane, teraz wzbogacone o dokładne współrzędne GPS (X i Y)
# Przykładowe współrzędne dla Bieszczad, żebyśmy mieli fajną mapę.
wydzielenia_gps = [
    {
        "id_dzialki": "10A",
        "gatunek": "Sosna",
        "powierzchnia_ha": 2.5,
        "x_lon": 22.545,  # Długość geograficzna (Wschód)
        "y_lat": 49.212   # Szerokość geograficzna (Północ)
    },
    {
        "id_dzialki": "12B",
        "gatunek": "Dąb",
        "powierzchnia_ha": 1.8,
        "x_lon": 22.548,
        "y_lat": 49.215
    },
    {
        "id_dzialki": "14C",
        "gatunek": "Świerk",
        "powierzchnia_ha": 3.2,
        "x_lon": 22.540,
        "y_lat": 49.210
    }
]

# 2. Tworzymy standardową tabelę Pandas (to, co znasz z wczoraj)
tabela = pd.DataFrame(wydzielenia_gps)

# 3. KROK MAGII GIS: Tworzymy Geometrię
# Shapely bierze X i Y z naszej tabeli i "klei" z nich Punkt (Point)
geometria = [Point(xy) for xy in zip(tabela["x_lon"], tabela["y_lat"])]

# 4. Tworzymy GeoDataFrame – Tabelę Przestrzenną!
# EPSG:4326 to kod określający globalny układ współrzędnych (WGS84), używany np. w Google Maps.
tabela_przestrzenna = gpd.GeoDataFrame(tabela, geometry=geometria, crs="EPSG:4326")

print("Zwróć uwagę na nową, magiczną kolumnę na samym końcu (geometry):")
print(tabela_przestrzenna)
print("-" * 50)

# 5. Eksport do formatu GeoJSON (standard czytelny dla QGIS i przeglądarek)
plik_wyjsciowy = "moje_wydzielenia.geojson"
tabela_przestrzenna.to_file(plik_wyjsciowy, driver="GeoJSON")

print(f"✅ Sukces! Plik wygenerowany i zapisany jako: {plik_wyjsciowy}")
print("To nie jest już tylko plik tekstowy. To pełnoprawna, leśna mapa przestrzenna!")