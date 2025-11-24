import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carga el archivo CSV "" en un DataFrame de pandas.
df = pd.read_csv("spotify_songs.csv")

# Muestra un título y una descripción en la aplicación Streamlit.
st.write("""
# Mi primera aplicación interactiva
## Gráficos usando la base de datos del Titanic
""")

