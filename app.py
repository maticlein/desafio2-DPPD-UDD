import streamlit as st
import pandas as pd
from modules.custom_plots import progress_plot
from PIL import Image

favicon = Image.open('./img/logo_UDD.png')

st.set_page_config(
    page_title = 'Desafío 2 - DPPD',
    page_icon = favicon,
    layout = 'centered',
    initial_sidebar_state = 'expanded'
)

col1, col2, col3 = st.columns(3)
logo = Image.open('./img/logo_UDD.png')
col2.image(logo, width = 200)  

st.header("Desafío 2 - Desarrollo de Proyectos y Productos de Datos")

df = pd.read_csv("./data/salarios.csv")

col1, col2 = st.columns(2)
col1.line_chart(df["Aexperiencia"])
col1.number_input(label = "Alarma Mínima Temp", min_value = 0, max_value = 100)
col1.number_input(label = "Alarma Máxima Temp", min_value = 0, max_value = 100)
col1.plotly_chart(progress_plot(23, "Temperatura"), use_container_width=True)

col2.line_chart(df["Salario"])
col2.number_input(label = "Alarma Mínima Hum", min_value = 0, max_value = 100)
col2.number_input(label = "Alarma Máxima Hum", min_value = 0, max_value = 100)
col2.plotly_chart(progress_plot(75, "Humedad"), use_container_width=True)

st.text_input(label = "Ingrese su mail:")

if st.button(label = "Enviar alarma"):
    st.write("Alarma enviada al email")