import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
import requests

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Geoprocessing BDL", layout="wide")
st.title("🌲 Interaktywny Kalkulator Stref Ochronnych")
# --- 1.5. BIZNESOWY OPIS PROJEKTU ---
with st.expander("ℹ️ Architektura i cel biznesowy projektu", expanded=False):
    st.markdown("""
    System służy do automatyzacji obliczeń powierzchni wyłączonej z produkcji leśnej.
    * **Silnik analityczny:** `Geopandas` (geometria przestrzenna na żywo).
    * **Integracja danych:** Bezpośrednie połączenie REST API z serwerami Banku Danych o Lasach (WMS).
    * **Wartość:** Redukcja czasu analizy kolizji z kilku godzin (ręczna praca w programach GIS) do ułamków sekund.
    """)

# --- 2. PANEL STEROWANIA ---
st.sidebar.header("⚙️ Parametry Analizy")
promien = st.sidebar.slider("Promień strefy ochronnej (metry):", min_value=10, max_value=100, value=30, step=5)
st.sidebar.markdown("---")
st.sidebar.write("📍 **Współrzędne drzewa:**")
lat = st.sidebar.number_input("Szerokość (Lat):", value=51.1320, format="%.4f")
lon = st.sidebar.number_input("Długość (Lon):", value=20.8650, format="%.4f")

# Nasz nowy włącznik silnika
uruchom = st.sidebar.button("🚀 Rozpocznij Analizę")

# --- 3. LOGIKA POBIERANIA DANYCH API ---
def pobierz_bdl(lat, lon):
    xmin, ymin = lon - 0.02, lat - 0.02
    xmax, ymax = lon + 0.02, lat + 0.02
    url = "https://mapserver.bdl.lasy.gov.pl/arcgis/rest/services/WMS_BDL/MapServer/5/query"
    parametry = {
        "where": "1=1", "outFields": "*", "f": "geojson",
        "geometry": f"{xmin},{ymin},{xmax},{ymax}",
        "geometryType": "esriGeometryEnvelope", "inSR": "4326"
    }
    return requests.get(url, params=parametry).json()

# INICJALIZACJA PAMIĘCI (Session State)
if "dane_lasu" not in st.session_state:
    st.session_state.dane_lasu = None

# Uruchomienie akcji po kliknięciu przycisku
if uruchom:
    with st.spinner("Łączę z serwerami BDL..."):
        # Zamiast do zwykłej zmiennej, zapisujemy wynik na stałe w pamięci aplikacji
        st.session_state.dane_lasu = pobierz_bdl(lat, lon)

# --- 4. OBLICZENIA GEOPRZESTRZENNE I MAPA (Fuzja) ---
mapa = folium.Map(location=[lat, lon], zoom_start=15, tiles="CartoDB positron")

# Jeśli mamy w pamięci pobrane dane z BDL, odpalamy silnik analityczny!
if st.session_state.dane_lasu and "features" in st.session_state.dane_lasu and len(st.session_state.dane_lasu["features"]) > 0:
    dane = st.session_state.dane_lasu
    
    # A. Tłumaczymy surowe dane BDL na obiekty matematyczne i metry
    wydzielenia_gdf = gpd.GeoDataFrame.from_features(dane["features"], crs="EPSG:4326")
    wydzielenia_metry = wydzielenia_gdf.to_crs(epsg=2180)
    
    # B. Tworzymy geometrię naszego drzewa
    drzewo_punkt = Point(lon, lat)
    drzewo_gdf = gpd.GeoDataFrame(geometry=[drzewo_punkt], crs="EPSG:4326")
    drzewo_metry = drzewo_gdf.to_crs(epsg=2180)
    
    # C. Generujemy strefę ochronną ("puchnięcie" punktu w metrach z suwaka)
    strefa_metry = drzewo_metry.buffer(promien)
    strefa_gdf = gpd.GeoDataFrame(geometry=strefa_metry, crs="EPSG:2180")
    
    # D. TWARDE PRZECIĘCIE (Intersection) - zderzamy las ze strefą
    kolizje = gpd.overlay(wydzielenia_metry, strefa_gdf, how='intersection')
    
    # --- 5. WIZUALIZACJA ---
    # Rysujemy prawdziwe lasy (na pomarańczowo)
    folium.GeoJson(
        dane, 
        name="Wydzielenia Gospodarcze",
        style_function=lambda x: {'fillColor': 'orange', 'color': 'darkorange', 'weight': 1, 'fillOpacity': 0.3}
    ).add_to(mapa)
    
    # Rysujemy Twoją strefę ochronną (na zielono)
    folium.GeoJson(
        strefa_gdf.to_crs(epsg=4326),
        name="Strefa Ochronna",
        style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'weight': 2, 'fillOpacity': 0.6}
    ).add_to(mapa)

    # Rysujemy sam punkt drzewa
    folium.Marker([lat, lon], popup="Twoje Drzewo Biocenotyczne", icon=folium.Icon(color="green")).add_to(mapa)

    # Wyświetlamy mapę
    st_folium(mapa, width=1000, height=500)
    
    # --- 6. GENEROWANIE RAPORTU W STREAMLIT ---
    st.markdown("### 📊 Raport Wyłączeń z Produkcji")
    
    if not kolizje.empty:
        st.error("⚠️ Wykryto kolizję! Strefa ochronna wchodzi na tereny gospodarcze.")
        
        # Obliczanie strat w hektarach i arach
        kolizje['Wyłączono [ha]'] = round(kolizje.geometry.area / 10000, 4)
        kolizje['Wyłączono [ary]'] = round(kolizje.geometry.area / 100, 2)
        
        # Filtrowanie tabeli do wyświetlenia dla Leśnika
        kolumny = ['Wyłączono [ha]', 'Wyłączono [ary]']
        if 'adress_forest' in kolizje.columns:
            kolizje['Adres Leśny'] = kolizje['adress_forest']
            kolumny.insert(0, 'Adres Leśny')
            
        # Pokaż piękną, interaktywną tabelę w przeglądarce
        st.dataframe(kolizje[kolumny], width="stretch")
    else:
        st.success("✅ Brak kolizji! Strefa ochronna jest bezpieczna i nie wymaga wyłączeń gospodarczych.")

else:
    # Jeśli użytkownik jeszcze nic nie pobrał, pokazujemy tylko pustą mapę
    folium.Marker([lat, lon], popup="Wybrane Drzewo", icon=folium.Icon(color="green")).add_to(mapa)
    st_folium(mapa, width=1000, height=500)
    st.info("👆 Użyj przycisku 'Rozpocznij Analizę' w panelu bocznym, aby pobrać mapę dla tej lokalizacji.")