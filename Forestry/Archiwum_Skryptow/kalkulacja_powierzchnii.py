import geopandas as gpd

print("📐 Projekt Portfolio #1: Analityka Przestrzenna")
print("-" * 60)

# 1. Wczytujemy wyizolowany obszar z poprzedniego skryptu
plik_wejsciowy = "nadlesnictwo_daleszyce.geojson"
obszar = gpd.read_file(plik_wejsciowy)

# 2. TRANSFORMACJA UKŁADU WSPÓŁRZĘDNYCH (CRS)
# Zmieniamy układ ze sferycznego GPS (EPSG:4326) na polski, płaski układ metrowy (EPSG:2180)
obszar_plaski = obszar.to_crs("EPSG:2180")

# 3. KALKULACJA (Prawdziwa inżynieria)
# Obliczamy pole powierzchni (area) dla płaskiej mapy. Wynik domyślnie jest w metrach kwadratowych.
powierzchnia_m2 = obszar_plaski.geometry.area.iloc[0]

# Zamieniamy metry kwadratowe na hektary (dzieląc przez 10 000) i zaokrąglamy do 2 miejsc po przecinku
powierzchnia_ha = round(powierzchnia_m2 / 10000, 2)

print(f"🌲 Analizowany obszar: {obszar['inspectorate_name'].iloc[0]}")
print(f"📏 Wyliczona matematycznie powierzchnia z granic obiektu: {powierzchnia_ha} ha")
print("-" * 60)