import pandas as pd

print("🌲 Baza Danych: Wydzielenia Leśne")
print("-" * 40)

wydzielenia = [
    {
        "id_dzialki": "10A",
        "gatunek": "Sosna",
        "powierzchnia_ha": 2.5,
        "gotowa_do_zrywki": False
    },
    {
        "id_dzialki": "12B",
        "gatunek": "Dąb",
        "powierzchnia_ha": 1.8,
        "gotowa_do_zrywki": True
    },
    {
        "id_dzialki": "14C",
        "gatunek": "Świerk",
        "powierzchnia_ha": 3.2,
        "gotowa_do_zrywki": False
    }
]

print("1. Wyciągamy konkretną informację z jednej rubryki:")
gatunek_drugiej = wydzielenia[1]["gatunek"]
print(f"Gatunek na drugiej działce to: {gatunek_drugiej}")
print("-" * 40)

print("2. Uruchamiamy automatyczną pętlę-filtrującą:")
for dzialka in wydzielenia:
    if dzialka["gotowa_do_zrywki"] == True:
        print(f"⚠️ UWAGA: Działka {dzialka['id_dzialki']} ({dzialka['gatunek']}) jest gotowa do wycinki!")

# --- NOWA SEKCJA GENERUJĄCA PLIK ---
print("\n3. Generowanie raportu do Excela...")
tabela = pd.DataFrame(wydzielenia)
tabela.to_csv("raport_dzialki.csv", index=False, sep=";")
print("✅ Gotowe! Plik raport_dzialki.csv czeka w folderze.")