import pandas as pd
import re

# Symulowana baza danych ogłoszeń z portali leśnych / BIP Nadleśnictw
# W przyszłości Python będzie pobierał te teksty bezpośrednio z sieci!
ogloszenia_bip = [
    {
        "id": "OGL-2026-001",
        "nadlesnictwo": "Nadleśnictwo Kielce",
        "tresc": "Przetarg na pozyskanie i zrywkę drewna w roku 2026 na terenie leśnictwa Dyminy. Wymagany sprzęt: harwester oraz forwarder."
    },
    {
        "id": "OGL-2026-002",
        "nadlesnictwo": "Nadleśnictwo Radom",
        "tresc": "Zapytanie ofertowe na wykonanie usług z zakresu szacunków brakarskich oraz wykonanie pomiarów struktury drzewostanu przy użyciu naziemnego skaningu laserowego (TLS)."
    },
    {
        "id": "OGL-2026-003",
        "nadlesnictwo": "Nadleśnictwo Suchedniów",
        "tresc": "Przetarg na zakup sadzonek sosny zwyczajnej oraz świerka pospolitego do odnowień leśnych."
    },
    {
        "id": "OGL-2026-004",
        "nadlesnictwo": "Nadleśnictwo Zagnańsk",
        "tresc": "Zlecenia na inwentaryzację zapasów drewna na powierzchniach badawczych. Preferowane metody teledetekcyjne oraz naziemny skaning laserowy TLS."
    }
]

def analizuj_ogloszenia(lista_ogloszen):
    print("🌲 Analizuję leśne bazy danych pod kątem zleceń premium...")
    print("=" * 60)
    
    raport_koncowy = []
    
    for ogl in lista_ogloszen:
        tekst = ogl["tresc"].lower()
        
        # Definiujemy słowa kluczowe, które nas interesują (projekty wysokopłatne)
        szukane_frazy = ["tls", "skaning", "skaningu", "pozyskanie drewna", "harwester"]
        
        dopasowania = [fraza for fraza in szukane_frazy if fraza in tekst]
        
        if dopasowania:
            print(f"🎯 Trafienie w {ogl['nadlesnictwo']}! Znalezione frazy: {dopasowania}")
            
            # Określamy typ projektu na podstawie znalezionych słów
            if "tls" in dopasowania or "skaning" in dopasowania:
                typ_projektu = "Technologia premium (TLS / Teledetekcja)"
            else:
                typ_projektu = "Usługi Leśne (ZUL)"
                
            raport_koncowy.append({
                "ID Ogłoszenia": ogl["id"],
                "Jednostka": ogl["nadlesnictwo"],
                "Typ Projektu": typ_projektu,
                "Dopasowane Słowa": ", ".join(dopasowania),
                "Status": "PILNE - Wyślij ofertę"
            })
        else:
            print(f"ℹ️ {ogl['nadlesnictwo']}: Brak interesujących tematów.")
            
    return raport_koncowy

if __name__ == "__main__":
    # Uruchamiamy analizę
    wyniki_analizy = analizuj_ogloszenia(ogloszenia_bip)
    
    print("=" * 60)
    # Zamieniamy wyniki w tabelę Pandas
    df_lesne = pd.DataFrame(wyniki_analizy)
    
    # Zapisujemy do dedykowanego pliku Excel/CSV
    nazwa_pliku = "raport_przetargow_lesnych.csv"
    df_lesne.to_csv(nazwa_pliku, index=False, encoding="utf-8-sig", sep=";")
    
    print(f"\n🎉 Raport ForestryTech wygenerowany i zapisany do: {nazwa_pliku}")
    print(df_lesne)