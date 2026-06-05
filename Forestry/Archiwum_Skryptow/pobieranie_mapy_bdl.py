import requests
import geopandas as gpd

print("🌲 Projekt Portfolio #1: Eksport geometrii Nadleśnictw (BDL)")
print("-" * 60)

url_bdl_mapa = "https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items?f=json&limit=500"

try:
    # KROK 1: EXTRACT (Pobranie niezawodnym requests)
    print("📡 Krok 1: Łączenie z API Lasów Państwowych...")
    odpowiedz = requests.get(url_bdl_mapa, timeout=30) # Dałem 30 sekund, bo pobieramy całą Polskę
    
    if odpowiedz.status_code == 200:
        print("✅ Pobrano dane. Zrzucam do warstwy buforowej na dysku...")
        
        # Zapisujemy surowy strumień z internetu do pliku roboczego
        plik_surowy = "surowe_bdl.geojson"
        with open(plik_surowy, "w", encoding="utf-8") as plik:
            plik.write(odpowiedz.text)
            
        # KROK 2: LOAD & TRANSFORM (Wczytanie mapy z dysku)
        print("🗂️ Krok 2: Geopandas buduje mapę z pliku lokalnego...")
        mapa_nadlesnictw = gpd.read_file(plik_surowy)
        
        print(f"✅ Sukces! Pobrane obiekty: {len(mapa_nadlesnictw)}")
        print(f"📊 Dostępne atrybuty: {list(mapa_nadlesnictw.columns)}")
        print("-" * 60)
        
        # KROK 3: Ostateczny eksport czystej mapy
        plik_wyjsciowy = "polskie_nadlesnictwa.geojson"
        print(f"💾 Trwa zapisywanie ostatecznej mapy jako {plik_wyjsciowy}...")
        mapa_nadlesnictw.to_file(plik_wyjsciowy, driver="GeoJSON")
        
        print("🎉 Misja zakończona. Plik przestrzenny jest gotowy!")
        
    else:
        print(f"❌ Serwer odrzucił zapytanie. Kod: {odpowiedz.status_code}")

except Exception as e:
    print(f"❌ Wystąpił krytyczny błąd mapowania: {e}")