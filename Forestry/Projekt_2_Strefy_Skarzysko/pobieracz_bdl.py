import requests
import json
import geopandas as gpd

print("🌲 Uruchamiam Konektor API Banku Danych o Lasach...")

# 1. Definiujemy obszar zainteresowania (Bounding Box)
# Tworzymy wirtualny prostokąt, który obejmuje z zapasem naszego Dęba i Jodłę
xmin, ymin = 20.83, 51.10
xmax, ymax = 20.88, 51.14

# 2. Budujemy żądanie do serwerów ESRI Lasów Państwowych
# Warstwa "5" to w systemie BDL szczegółowe "Wydzielenia"
url = "https://mapserver.bdl.lasy.gov.pl/arcgis/rest/services/WMS_BDL/MapServer/5/query"

parametry = {
    "where": "1=1",
    "outFields": "*",
    "geometry": f"{xmin},{ymin},{xmax},{ymax}",
    "geometryType": "esriGeometryEnvelope",
    "inSR": "4326",
    "spatialRel": "esriSpatialRelIntersects",
    "f": "geojson"
}

# 3. Połączenie z serwerem w locie
print(f"📡 Łączenie z serwerami BDL. Pobieranie geometrii dla obszaru Skarżyska...")
odpowiedz = requests.get(url, params=parametry)

if odpowiedz.status_code == 200:
    dane_geojson = odpowiedz.json()
    
    # Zabezpieczenie przed pustym wynikiem
    if "features" in dane_geojson and len(dane_geojson["features"]) > 0:
        # 4. Zapis surowych danych do pliku w Twoim folderze
        nazwa_pliku = "prawdziwe_wydzielenia_skarzysko.geojson"
        with open(nazwa_pliku, 'w', encoding='utf-8') as plik:
            json.dump(dane_geojson, plik, ensure_ascii=False)
            
        print(f"✅ Sukces! Zapisano plik: {nazwa_pliku}")
        
        # 5. Szybki raport inżynieryjny z pobranej paczki
        gdf = gpd.read_file(nazwa_pliku)
        print(f"📊 Pobrano i zmapowano {len(gdf)} prawdziwych wydzieleń leśnych.")
    else:
        print("⚠️ Serwer odpowiedział, ale nie znalazł żadnych wydzieleń w tym kwadracie.")
else:
    print(f"❌ Błąd krytyczny połączenia z BDL. Kod błędu: {odpowiedz.status_code}")