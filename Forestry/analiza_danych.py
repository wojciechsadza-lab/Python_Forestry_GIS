import pandas as pd

print("📊 Uruchamiam Moduł Analityczny ForestryTech...")
print("-" * 50)

# 1. ODCZYT: Wczytujemy wczorajszy plik CSV z dysku z powrotem do Pythona.
# Używamy sep=";", bo takim znakiem oddzieliliśmy kolumny przy zapisie.
tabela = pd.read_csv("raport_dzialki.csv", sep=";")

print("Oto dane wczytane prosto z pliku:")
print(tabela)
print("-" * 50)

# 2. FILTROWANIE BEZ PĘTLI:
# Wyciągamy z bazy TYLKO te działki, które mają status gotowych do zrywki.
# Pandas robi to jedną komendą, odrzucając resztę!
dzialki_do_ciecia = tabela[tabela["gotowa_do_zrywki"] == True]

print("⚠️ Znaleziono działki gotowe do zrywki:")
print(dzialki_do_ciecia)
print("-" * 50)

# 3. MATEMATYKA NA DANYCH:
# Sumujemy wszystkie wartości w kolumnie "powierzchnia_ha"
laczna_powierzchnia = tabela["powierzchnia_ha"].sum()

# Wyciągamy najwyższą (maksymalną) wartość z tej samej kolumny
najwieksza_dzialka = tabela["powierzchnia_ha"].max()

print(f"🌲 Łączna powierzchnia Twoich wydzieleń to: {laczna_powierzchnia} ha")
print(f"👑 Największa pojedyncza działka ma: {najwieksza_dzialka} ha")
print("-" * 50)
# --- NOWA SEKCJA ---
print("\n4. ZAAWANSOWANA ANALIZA: Grupowanie danych")

# Grupujemy tabelę po kolumnie "gatunek", a następnie sumujemy dla nich "powierzchnia_ha"
powierzchnia_wedlug_gatunkow = tabela.groupby("gatunek")["powierzchnia_ha"].sum()

print("Powierzchnia lasu z podziałem na gatunki drzew:")
print(powierzchnia_wedlug_gatunkow)
print("-" * 50)