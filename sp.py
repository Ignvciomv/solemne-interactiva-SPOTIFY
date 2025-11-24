import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt 

# -----------------------------
# CARGA DE DATOS
# -----------------------------
@st.cache_data
def load_data():
df = pd.read_csv("spotify_songs.csv")

# Convertimos la fecha a tipo datetime y sacamos el año
df["track_album_release_date"] = pd.to_datetime(
df["track_album_release_date"], errors="coerce"
)
df["year"] = df["track_album_release_date"].dt.year

return df


df = load_data()

# -----------------------------
# CONFIGURACIÓN BÁSICA DE LA APP
# -----------------------------
st.set_page_config(
page_title="Spotify Songs Explorer",
page_icon="🎵",
layout="wide"
)

st.title("🎧 Explorador interactivo de canciones de Spotify")
st.write(
"Esta página te permite filtrar, explorar y visualizar el dataset "
"`spotify_songs.csv` de Kaggle."
)

# -----------------------------
# SIDEBAR: FILTROS
# -----------------------------
st.sidebar.header("Filtros")

# Filtro por género de playlist
all_genres = sorted(df["playlist_genre"].dropna().unique().tolist())
selected_genres = st.sidebar.multiselect(
"Género de playlist",
options=all_genres,
default=all_genres # por defecto todos
)

# Filtro por subgénero (dependiente del género)
if selected_genres:
df_genre_filtered = df[df["playlist_genre"].isin(selected_genres)]
else:
df_genre_filtered = df.copy()

all_subgenres = sorted(df_genre_filtered["playlist_subgenre"].dropna().unique().tolist())
selected_subgenres = st.sidebar.multiselect(
"Subgénero de playlist",
options=all_subgenres,
default=all_subgenres
)

# Rango de años
min_year = int(df["year"].min())
max_year = int(df["year"].max())
year_range = st.sidebar.slider(
"Año de lanzamiento",
min_value=min_year,
max_value=max_year,
value=(min_year, max_year)
)

# Rango de popularidad
pop_range = st.sidebar.slider(
"Popularidad de la canción (0–100)",
min_value=0,
max_value=100,
value=(0, 100)
)

# Filtro por artista (opcional)
all_artists = sorted(df_genre_filtered["track_artist"].dropna().unique().tolist())
selected_artist = st.sidebar.selectbox(
"Filtrar por artista (opcional)",
options=["Todos"] + all_artists,
index=0
)

# -----------------------------
# APLICAR FILTROS
# -----------------------------
df_filtered = df.copy()

if selected_genres:
df_filtered = df_filtered[df_filtered["playlist_genre"].isin(selected_genres)]

if selected_subgenres:
df_filtered = df_filtered[df_filtered["playlist_subgenre"].isin(selected_subgenres)]

df_filtered = df_filtered[
(df_filtered["year"].between(year_range[0], year_range[1])) &
(df_filtered["track_popularity"].between(pop_range[0], pop_range[1]))
]

if selected_artist != "Todos":
df_filtered = df_filtered[df_filtered["track_artist"] == selected_artist]

# -----------------------------
# MÉTRICAS RESUMEN
# -----------------------------
st.subheader("Resumen de las canciones filtradas")

col1, col2, col3 = st.columns(3)

num_tracks = len(df_filtered)
avg_popularity = df_filtered["track_popularity"].mean() if num_tracks > 0 else 0
avg_danceability = df_filtered["danceability"].mean() if num_tracks > 0 else 0

col1.metric("Número de canciones", f"{num_tracks}")
col2.metric("Popularidad promedio", f"{avg_popularity:.1f}")
col3.metric("Danceability promedio", f"{avg_danceability:.2f}")

st.markdown("---")

# -----------------------------
# TABLA DE CANCIONES
# -----------------------------
st.subheader("Canciones (Top 50 por popularidad)")

if num_tracks == 0:
st.warning("No hay canciones que cumplan con los filtros seleccionados.")
else:
df_top = (
df_filtered.sort_values("track_popularity", ascending=False)
.head(50)[[
"track_name",
"track_artist",
"track_popularity",
"playlist_genre",
"playlist_subgenre",
"year"
]]
)
st.dataframe(df_top, use_container_width=True)

# -----------------------------
# GRÁFICOS INTERACTIVOS
# -----------------------------
st.markdown("---")
st.subheader("Visualización interactiva")

if num_tracks > 0:
numeric_columns = [
"danceability", "energy", "valence", "tempo",
"duration_ms", "track_popularity", "loudness"
]

col_x, col_y = st.columns(2)
x_var = col_x.selectbox("Eje X", options=numeric_columns, index=0)
y_var = col_y.selectbox("Eje Y", options=numeric_columns, index=1)

chart = (
alt.Chart(df_filtered)
.mark_circle(opacity=0.6)
.encode(
x=alt.X(x_var, title=x_var.capitalize()),
y=alt.Y(y_var, title=y_var.capitalize()),
color=alt.Color("playlist_genre", title="Género"),
tooltip=[
"track_name",
"track_artist",
"track_popularity",
"playlist_genre",
"playlist_subgenre",
"year"
]
)
.interactive()
)

st.altair_chart(chart, use_container_width=True)

st.caption(
"Puedes cambiar las variables de los ejes en los selectores de arriba para "
"explorar diferentes relaciones (por ejemplo, Popularidad vs Energy, "
"Danceability vs Valence, etc.)."
)

else:
st.info("Ajusta los filtros en la barra lateral para ver gráficos.")