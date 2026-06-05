import requests

print("🌲 Projekt Portfolio #1: Konektor BDL")
print("-" * 60)

# NOWY, oficjalny i aktualny punkt dostępowy API dla polskich nadleśnictw
url_bdl = "https://ogcapi.bdl.lasy.gov.pl/collections/nadlesnictwa/items?f=json"

try:
    print("📡 Wysyłam zapytanie do serwerów Lasów Państwowych (OGC API)...")
    odpowiedz = requests.get(url_bdl, timeout=15)
    
    if odpowiedz.status_code == 200:
        print("✅ Sukces! Zalogowano do nowej bazy BDL.")
        
        dane_bdl = odpowiedz.json()
        
        # W nowym standardzie BDL, lista nadleśnictw znajduje się pod kluczem 'features'
        nadlesnictwa = dane_bdl['features']
        
        print(f"📊 Serwer zwrócił dane o {len(nadlesnictwa)} nadleśnictwach z całej Polski.")
        
        # DEBUGGOWANIE: Wyciągamy pierwsze nadleśnictwo z brzegu i zaglądamy w jego atrybuty ('properties')
        print("\n🔍 Struktura pobranych danych (Atrybuty pojedynczego nadleśnictwa):")
        print(nadlesnictwa[0]['properties'])
        print("-" * 60)
        
    else:
        print(f"❌ Odmowa dostępu. Kod błędu serwera: {odpowiedz.status_code}")

except Exception as e:
    print(f"❌ Awaria systemu łączności: {e}")