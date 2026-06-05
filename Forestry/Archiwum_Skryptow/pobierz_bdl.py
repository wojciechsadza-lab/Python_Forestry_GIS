import requests
import geopandas as gpd

print("🌐 Łączenie z zewnętrznym serwerem danych...")
print("-" * 60)

url_api = "https://raw.githubusercontent.com/datasets/geo-boundaries-world-110m/master/countries.geojson"

try:
    print("📡 Wysyłam zapytanie do API...")
    odpowiedz = requests.get(url_api, timeout=15)
    
    if odpowiedz.status_code == 200:
        print("✅ Dane dotarły! Zrzucam surowy plik z internetu na dysk...")
        
        # 1. Zapisujemy surowe dane z internetu BEZPOŚREDNIO do pliku tekstowego
        nazwa_surowa = "surowe_dane_z_sieci.geojson"
        with open(nazwa_surowa, "w", encoding="utf-8") as plik:
            plik.write(odpowiedz.text)
            
        print(f"💾 Zapisano na dysku jako: {nazwa_surowa}. Rozpoczynam analizę GIS...")
        
        # 2. Geopandas na spokojnie wczytuje i układa dane z fizycznego pliku
        tabela_przestrzenna = gpd.read_file(nazwa_surowa)
        
        print("\n📊 Struktura pobranej bazy danych (pierwsze 3 wiersze):")
        print(tabela_przestrzenna.head(3))
        print("-" * 60)
        print("🎉 MISJA ZAKOŃCZONA SUKCESEM!")
        
    else:
        print(f"❌ Serwer zwrócił błąd. Kod: {odpowiedz.status_code}")

except Exception as e:
    print(f"❌ Wystąpił błąd: {e}")