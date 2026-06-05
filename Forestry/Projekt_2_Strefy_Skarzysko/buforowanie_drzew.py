import geopandas as gpd
from shapely.geometry import Point

# 1. Definiujemy lokalizacje naszych cennych drzew w Nadleśnictwie Skarżysko
# (Zaktualizowane współrzędne wycelowane w środek wydzieleń leśnych)
drzewa_dane = [
    {"id": "Dąb_Skarżysko_1", "lon": 20.8400, "lat": 51.1280, "gatunek": "Dąb szypułkowy"},
    {"id": "Jodła_Skarżysko_2", "lon": 20.8650, "lat": 51.1320, "gatunek": "Jodła pospolita"}
]

# 2. Przekształcamy surowe dane w matematyczne obiekty przestrzenne (PUNKTY)
geometria = [Point(drzewo['lon'], drzewo['lat']) for drzewo in drzewa_dane]
drzewa_gdf = gpd.GeoDataFrame(drzewa_dane, geometry=geometria, crs="EPSG:4326")

print("✅ System wczytał współrzędne drzew z Nadleśnictwa Skarżysko:")
print(drzewa_gdf[['id', 'gatunek', 'geometry']])

# 3. Transformacja do polskiego układu (EPSG:2180), gdzie jednostką są METRY
drzewa_metry = drzewa_gdf.to_crs(epsg=2180)

# 4. Wyznaczanie ścisłej strefy ochronnej (promień 30 metrów od pnia)
# Funkcja .buffer(30) matematycznie "puchnie" punkt do okręgu o podanym promieniu
strefy_ochronne_metry = drzewa_metry.copy()
strefy_ochronne_metry['geometry'] = strefy_ochronne_metry.geometry.buffer(30)

# 5. Obliczenie dokładnej powierzchni wyłączonej z wycinki
# Powierzchnia koła: Pi * r^2. Dla 30m powinno wyjść około 2827 m2.
strefy_ochronne_metry['powierzchnia_m2'] = strefy_ochronne_metry.geometry.area

print("\n✅ System wyznaczył strefy ochronne w układzie metrycznym:")
print(strefy_ochronne_metry[['id', 'gatunek', 'powierzchnia_m2']])

from shapely.geometry import Polygon

# 6. Wczytanie prawdziwej mapy wydzieleń z dysku (Nadleśnictwo Skarżysko)
print("🌲 Ładowanie prawdziwych granic wydzieleń BDL...")
prawdziwy_las_gdf = gpd.read_file("prawdziwe_wydzielenia_skarzysko.geojson")

# API z BDL zwróciło angielskie nazwy - filtrujemy je
wydzielenia_gdf = prawdziwy_las_gdf[['adress_forest', 'forest_func_cd', 'geometry']].copy()

# Zmieniamy nazwy kolumn na polskie, żeby raport był czytelny
wydzielenia_gdf.rename(columns={
    'adress_forest': 'adres_lesny', 
    'forest_func_cd': 'typ'
}, inplace=True)

# Tłumaczymy układ współrzędnych z GPS na metry (EPSG:2180)
wydzielenia_gdf = wydzielenia_gdf.to_crs(epsg=2180)

# 7. PRZECIĘCIE WARSTW (Intersection) - Fuzja danych
kolizje = gpd.overlay(wydzielenia_gdf, strefy_ochronne_metry, how='intersection')

# Obliczamy pole powierzchni samego przecięcia
powierzchnia_m2 = kolizje.geometry.area

# Tłumaczymy to na język leśników (1 ha = 10 000 m2, 1 ar = 100 m2)
kolizje['powylaczona_ha'] = round(powierzchnia_m2 / 10000, 4)
kolizje['powylaczona_ary'] = round(powierzchnia_m2 / 100, 2)

print("\n🚨 RAPORT KOLIZJI (PRAWDZIWE DANE): Wydzielenia gospodarcze vs Strefy Ochronne")
print(kolizje[['adres_lesny', 'typ', 'id', 'powylaczona_ha', 'powylaczona_ary']])
import folium

# 8. WIZUALIZACJA WYNIKÓW NA INTERAKTYWNEJ MAPIE
print("\n🗺️ Generowanie mapy podglądowej na prawdziwych danych...")

# Środek mapy ustawiamy na okolice naszego Dęba w Skarżysku
mapa = folium.Map(location=[51.1200, 20.8500], zoom_start=15, tiles="CartoDB positron")

# Dodajemy prawdziwe wydzielenia gospodarcze pobrane z BDL
# (Musimy je cofnąć na układ GPS - EPSG:4326, żeby mapa je prawidłowo narysowała)
folium.GeoJson(
    wydzielenia_gdf.to_crs(epsg=4326),
    style_function=lambda x: {'fillColor': 'orange', 'color': 'darkorange', 'weight': 2, 'fillOpacity': 0.4},
    name="Prawdziwe Wydzielenia (BDL Skarżysko)"
).add_to(mapa)

# Dodajemy zielone strefy ochronne
folium.GeoJson(
    strefy_ochronne_metry.to_crs(epsg=4326),
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 2, 'fillOpacity': 0.6},
    name="Strefy Ochronne Drzew (30m)"
).add_to(mapa)

# Dodajemy kontroler warstw i zapisujemy plik
folium.LayerControl().add_to(mapa)
mapa.save("Mapa_Kolizji_Skarzysko.html")

print("✅ Mapa została wygenerowana! Otwórz plik 'Mapa_Kolizji_Skarzysko.html' w przeglądarce.")
import matplotlib.pyplot as plt
from fpdf import FPDF

# 9. AUTOMATYCZNY GENERATOR RAPORTU PDF
print("\n📊 Uruchamiam proces generowania oficjalnego raportu PDF...")

# A. Generowanie statycznego obrazu mapy do załącznika
fig, ax = plt.subplots(figsize=(8, 8))
# Rysujemy wydzielenia leśne
wydzielenia_gdf.plot(ax=ax, color='orange', alpha=0.4, edgecolor='darkorange', label='Wydzielenia BDL')
# Rysujemy strefy ochronne
strefy_ochronne_metry.plot(ax=ax, color='green', alpha=0.5, edgecolor='darkgreen', label='Strefy Ochronne')
# Jeśli są kolizje, zaznaczamy je na czerwono
if not kolizje.empty:
    kolizje.plot(ax=ax, color='red', alpha=0.8, edgecolor='darkred')

plt.title("Mapa Sytuacyjna - Strefy Ochronne Drzew Biocenotycznych\nNadleśnictwo Skarżysko", fontsize=12, pad=15)
ax.set_axis_off() # Ukrywamy osie wykresu, żeby wyglądało jak czysta mapa

sciezka_mapy = "mapa_raport.png"
plt.savefig(sciezka_mapy, dpi=300, bbox_inches='tight')
plt.close()
print("   -> Statyczna mapa załącznika została wygenerowana.")

# B. Tworzenie dokumentu PDF (Klasa FPDF)
pdf = FPDF()
pdf.add_page()

# Definiujemy standardową czcionkę (używamy wbudowanego Helvetica, bez polskich znaków na potrzeby szybkiego testu)
pdf.set_font("Helvetica", size=12)

# Nagłówek dokumentu
pdf.set_font("Helvetica", style="B", size=16)
pdf.cell(200, 10, txt="RAPORT WYLACZEN BIOCENOTYCZNYCH", ln=True, align="C")
pdf.cell(200, 10, txt="Jednostka organizacyjna: Nadlesnictwo Skarzysko", ln=True, align="C")
# ...
pdf.cell(200, 10, txt="1. Podsumowanie analizy przestrzennej:", ln=True)
pdf.ln(10) # Odstęp

# Treść główna raportu
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(200, 10, txt="1. Podsumowanie analizy przestrzennej:", ln=True)
pdf.set_font("Helvetica", size=11)

if not kolizje.empty:
    for index, row in kolizje.iterrows():
        tekst_wiersza = f"- Wykryto naruszenie w wydzieleniu gospodarczym: {row['adres_lesny']}\n" \
                        f"  Identyfikator drzewa: {row['id']}\n" \
                        f"  Powierzchnia wylaczona z uzytkowania: {row['powylaczona_ha']} ha ({row['powylaczona_ary']} a)"
        pdf.multi_cell(0, 8, txt=tekst_wiersza)
        pdf.ln(2)
else:
    pdf.cell(0, 10, txt="Brak nakladania sie stref ochronnych na wydzielenia lesne.", ln=True)

pdf.ln(10)

# Dodanie wygenerowanej mapy do dokumentu PDF
pdf.set_font("Helvetica", style="B", size=12)
pdf.cell(200, 10, txt="2. Załącznik kartograficzny (Lokalizacja kolizji):", ln=True)
pdf.image(sciezka_mapy, x=15, y=pdf.get_y() + 5, w=130)

# Zapis pliku na dysku
nazwa_raportu = "Oficjalny_Raport_Skarzysko.pdf"
pdf.output(nazwa_raportu)

print(f"✅ Sukces! Oficjalny dokument został zapisany jako: {nazwa_raportu}")