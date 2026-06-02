import geopandas as gpd
import folium

print("🌍 Projekt Portfolio #1: Generator Interaktywnej Mapy WebGIS")
print("-" * 60)

# 1. Wczytujemy naszą precyzyjną próbkę wydzieleń
plik_zrodlowy = "probka_wydzielen.geojson"
print(f"🗂️ Wczytuję dane przestrzenne z {plik_zrodlowy}...")
tabela_wydzielen = gpd.read_file(plik_zrodlowy)

# 2. BEZPIECZEŃSTWO WSPÓŁRZĘDNYCH
# Mapy internetowe (Google, OpenStreetMap) działają TYLKO w sferycznym układzie GPS (EPSG:4326).
# Upewniamy się, że nasze dane mają ten format, zanim wrzucimy je do internetu.
tabela_wydzielen = tabela_wydzielen.to_crs("EPSG:4326")

# 3. KALIBRACJA KAMERY
# Wyciągamy matematyczny środek (centroid) pierwszego wydzielenia, żeby kamera mapy
# wiedziała, w którym miejscu na kuli ziemskiej ma się ustawić po otwarciu pliku.
srodek_y = tabela_wydzielen.geometry.centroid.y.iloc[0]
srodek_x = tabela_wydzielen.geometry.centroid.x.iloc[0]

# 4. TWORZENIE BAZOWEJ MAPY
print("🗺️ Rysuję podkład satelitarny / mapowy...")
# Używamy jasnego, czystego podkładu 'CartoDB positron', który wygląda bardzo profesjonalnie w biznesie
mapa_biznesowa = folium.Map(location=[srodek_y, srodek_x], zoom_start=13, tiles="CartoDB positron")

# 5. NAKŁADANIE DANYCH (Z magią interaktywności)
print("✨ Nakładam poligony i konfiguruję wyskakujące okienka (Tooltips)...")
folium.GeoJson(
    tabela_wydzielen,
    name="Wydzielenia Leśne (BDL)",
    style_function=lambda feature: {
        'fillColor': '#2ca25f', # Profesjonalny, leśny odcień zieleni
        'color': 'black',       # Kolor granic wydzielenia
        'weight': 1,            # Grubość granicy
        'fillOpacity': 0.5      # Przezroczystość (żeby było widać co jest pod spodem)
    },
    # Konfigurujemy okienko, które wyskoczy po najechaniu myszką na las!
    tooltip=folium.GeoJsonTooltip(
        fields=["adr_for", "sub_area", "forest_fun", "rotat_age"],
        aliases=["Adres leśny:", "Powierzchnia (ha):", "Funkcja lasu:", "Wiek rębności:"],
        localize=True
    )
).add_to(mapa_biznesowa)

# Dodajemy przycisk w rogu do włączania/wyłączania warstw
folium.LayerControl().add_to(mapa_biznesowa)

# 6. ZAPIS DO PLIKU INTERNETOWEGO
nazwa_html = "portfolio_mapa.html"
mapa_biznesowa.save(nazwa_html)

print(f"🎉 GOTOWE! Wygenerowano w pełni klikalną mapę jako: {nazwa_html}")
print("👉 Kliknij na ten plik prawym przyciskiem myszy w VS Code, wybierz 'Reveal in Finder', a potem odpal go w Chrome lub Safari!")
print("-" * 60)