import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import plotly.express as px
import pandas as pd
import os

# ---------------------------------------------------------
# KONFIGURACJA UI (Premium)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Leśny Panel Analityczny",
    page_icon="🌲",
    layout="wide"
)

ukryj_style_streamlit = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(ukryj_style_streamlit, unsafe_allow_html=True)

st.title("🌲 System Analityki Przestrzennej Lasów Państwowych")
st.markdown("---")

# ---------------------------------------------------------
# 1. BACKEND: ŁADOWANIE DANYCH
# ---------------------------------------------------------
katalog_biezacy = os.path.dirname(__file__)
plik_geojson = os.path.join(katalog_biezacy, "probka_wydzielen.geojson")

try:
    dane_lesne = gpd.read_file(plik_geojson)
    dane_lesne = dane_lesne.to_crs("EPSG:4326")
    
    dane_lesne['forest_fun'] = dane_lesne['forest_fun'].fillna('Brak danych')
    dane_lesne['rotat_age'] = pd.to_numeric(dane_lesne['rotat_age'], errors='coerce').fillna(0)
    dane_lesne['sub_area'] = pd.to_numeric(dane_lesne['sub_area'], errors='coerce').fillna(0)
except Exception as e:
    st.error(f"Błąd ładowania pliku: {e}")
    st.stop()

# ---------------------------------------------------------
# 2. INTERFEJS BOCZNY
# ---------------------------------------------------------
st.sidebar.header("⚙️ Panel Sterowania")

with st.sidebar.expander("🔍 Zaawansowane Filtry", expanded=True):
    dostepne_funkcje = dane_lesne['forest_fun'].unique().tolist()
    wybrane_funkcje = st.multiselect("Funkcja lasu:", options=dostepne_funkcje, default=dostepne_funkcje)
    
    st.markdown("---")
    
    min_wiek, max_wiek = int(dane_lesne['rotat_age'].min()), int(dane_lesne['rotat_age'].max())
    wybrany_wiek = st.slider("Wiek rębności (lata):", min_value=min_wiek, max_value=max_wiek, value=(min_wiek, max_wiek))
    
    st.markdown("---")
    
    min_pow, max_pow = float(dane_lesne['sub_area'].min()), float(dane_lesne['sub_area'].max())
    wybrana_pow = st.slider("Powierzchnia (ha):", min_value=min_pow, max_value=max_pow, value=(min_pow, max_pow))

przefiltrowane_dane = dane_lesne[
    (dane_lesne['forest_fun'].isin(wybrane_funkcje)) &
    (dane_lesne['rotat_age'] >= wybrany_wiek[0]) & (dane_lesne['rotat_age'] <= wybrany_wiek[1]) &
    (dane_lesne['sub_area'] >= wybrana_pow[0]) & (dane_lesne['sub_area'] <= wybrana_pow[1])
]

kolory_funkcji = {'OCHR': '#006d2c', 'GOSP': '#74c476', 'Brak danych': '#969696'}

# ---------------------------------------------------------
# 3. KAFELKI KPI I ZAKŁADKI (TABS)
# ---------------------------------------------------------
if not przefiltrowane_dane.empty:
    st.subheader("📊 Główne Wskaźniki (KPI)")
    kol1, kol2, kol3, kol4 = st.columns(4) # Zmieniamy na 4 kolumny!
    
    kol1.metric("Suma Powierzchni", f"{przefiltrowane_dane['sub_area'].sum():.2f} ha")
    kol2.metric("Liczba Wydzieleń", len(przefiltrowane_dane))
    kol3.metric("Średni Wiek", f"{przefiltrowane_dane['rotat_age'].mean():.0f} lat")
    kol4.metric("Najstarsze Wydzielenie", f"{przefiltrowane_dane['rotat_age'].max():.0f} lat")
    
    st.markdown("---")
    
    kol_mapa, kol_wykres = st.columns([2, 1])
    
    with kol_wykres:
        st.subheader("📈 Analiza Szczegółowa")
        # NOWOŚĆ: System profesjonalnych zakładek
        zakladka1, zakladka2 = st.tabs(["Powierzchnia wg Funkcji", "Struktura Wieku"])
        
        with zakladka1:
            dane_do_wykresu = przefiltrowane_dane.groupby('forest_fun')['sub_area'].sum().reset_index()
            fig = px.bar(
                dane_do_wykresu, x='forest_fun', y='sub_area',
                color='forest_fun', color_discrete_map=kolory_funkcji, text_auto='.2f'
            )
            fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title="Powierzchnia (ha)")
            st.plotly_chart(fig, use_container_width=True)
            
        with zakladka2:
            # NOWOŚĆ: Wykres struktury wiekowej lasu
            fig2 = px.histogram(
                przefiltrowane_dane, x='rotat_age', nbins=10, 
                color_discrete_sequence=['#2ca25f'],
                labels={'rotat_age': 'Wiek rębności'}
            )
            fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_title="Liczba wydzieleń")
            st.plotly_chart(fig2, use_container_width=True)
            
        st.markdown("---")
        czyste_dane_csv = przefiltrowane_dane.drop(columns=['geometry'])
        st.download_button(
            label="📄 Pobierz Raport (.CSV)",
            data=czyste_dane_csv.to_csv(index=False).encode('utf-8'), 
            file_name='raport_lesny.csv', mime='text/csv', use_container_width=True 
        )

# ---------------------------------------------------------
# 4. FRONTEND: MAPA I TABELA ATRYBUTÓW
# ---------------------------------------------------------
    with kol_mapa:
        st.subheader("🗺️ Interaktywny Moduł Kartograficzny")
        
        mapa = folium.Map(tiles=None)
        bounds = przefiltrowane_dane.total_bounds
        mapa.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])
        
        folium.TileLayer('CartoDB positron', name='Mapa Jasna').add_to(mapa)
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri', name='Satelita (Esri)', overlay=False, control=True
        ).add_to(mapa)

        folium.GeoJson(
            przefiltrowane_dane, name="Wydzielenia",
            style_function=lambda feature: {
                'fillColor': kolory_funkcji.get(feature['properties']['forest_fun'], '#000000'),
                'color': 'black', 'weight': 1, 'fillOpacity': 0.7
            },
            tooltip=folium.GeoJsonTooltip(fields=["adr_for", "sub_area", "forest_fun", "rotat_age"], aliases=["Adres leśny:", "Powierzchnia (ha):", "Funkcja lasu:", "Wiek rębności:"], localize=True)
        ).add_to(mapa)
        
        folium.LayerControl(collapsed=False, position='topleft').add_to(mapa)
        st_folium(mapa, use_container_width=True, height=500)

    # NOWOŚĆ: Tabela Atrybutów na samym dole
    st.markdown("---")
    st.subheader("🗄️ Tabela Atrybutów (Surowe Dane)")
    with st.expander("Kliknij, aby rozwinąć i przeglądać tabelę danych"):
        # Wyświetlamy czystą, interaktywną tabelę wprost z biblioteki Pandas
        st.dataframe(czyste_dane_csv, use_container_width=True, hide_index=True)
        
else:
    st.warning("Brak danych spełniających wybrane kryteria. Zmień ustawienia w panelu bocznym.")