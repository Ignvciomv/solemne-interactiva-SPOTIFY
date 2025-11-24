import streamlit as st
import pandas as pd


# Carga el archivo CSV "" en un DataFrame de pandas.
df = pd.read_csv("spotify_songs.csv.zip")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

