import requests
import geopandas as gpd

print("🌲 Projekt Portfolio #1: Głęboka Analityka (Wydzielenia Leśne)")
print("-" * 60)

# NOWY ADRES: Uderzamy w konkretną partycję serwera (RDLP Radom), gdzie leżą Daleszyce
url_wydzielenia = "https://ogcapi.bdl.lasy.gov.pl/collections/RDLP_Radom_wydzielenia/items?f=json&limit=100"

try:
    print("📡 Krok 1: Łączenie z API (warstwa wydzieleń RDLP Radom)...")
    odpowiedz = requests.get(url_wydzielenia, timeout=30)
    
    if odpowiedz.status_code == 200:
        print("✅ Pobrano dane szczegółowe. Zrzucam do warstwy buforowej...")
        
        plik_surowy = "surowe_wydzielenia.geojson"
        with open(plik_surowy, "w", encoding="utf-8") as plik:
            plik.write(odpowiedz.text)
            
        print("🗂️ Krok 2: Geopandas wczytuje tabelę do pamięci RAM...")
        tabela_wydzielen = gpd.read_file(plik_surowy)
        
        print(f"📊 Sukces! Pobrane obiekty (wiersze): {len(tabela_wydzielen)}")
        
        print("\n🔍 Skanowanie twardych danych taksacyjnych. Dostępne atrybuty to:")
        # Przekształcamy listę kolumn na czytelniejszy, pionowy format
        for kolumna in tabela_wydzielen.columns:
            print(f"- {kolumna}")
        print("-" * 60)
        
        plik_wyjsciowy = "probka_wydzielen.geojson"
        tabela_wydzielen.to_file(plik_wyjsciowy, driver="GeoJSON")
        print(f"🎉 Zapisano precyzyjną geometrię wydzieleń jako: {plik_wyjsciowy}")
        
    else:
        print(f"❌ Serwer odrzucił zapytanie. Kod: {odpowiedz.status_code}")

except Exception as e:
    print(f"❌ Wystąpił krytyczny błąd pobierania: {e}")