import streamlit as st
import pandas as pd
from modules.custom_plots import progress_plot
from PIL import Image
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from streamlit_autorefresh import st_autorefresh

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

count = st_autorefresh(interval = 2000, debounce = True)

conn = st.experimental_connection('mysql', type='sql')
df = conn.query('SELECT * from tb_registro;', ttl=10)

sensor_temp = df[df["id_sensor"] == 1]
sensor_hum = df[df["id_sensor"] == 2]

last_temp = sensor_temp.iloc[-1]["sensor_value"]
last_hum = sensor_hum.iloc[-1]["sensor_value"]

col1, col2 = st.columns(2)
col1.plotly_chart(progress_plot(last_temp, "Temperatura", -30, 60), use_container_width=True)
col1.line_chart(sensor_temp["sensor_value"])
min_temp = col1.number_input(label = "Alarma Temperatura Mínima", min_value = -30, max_value = 60, value = 5)
max_temp = col1.number_input(label = "Alarma Temperatura Máxima", min_value = -30, max_value = 60, value = 40)

col2.plotly_chart(progress_plot(last_hum, "Humedad", 0, 100), use_container_width=True)
col2.line_chart(sensor_hum["sensor_value"])
min_hum = col2.number_input(label = "Alarma Humedad Mínima", min_value = 0, max_value = 100, value = 60)
max_hum = col2.number_input(label = "Alarma Humedad Máxima", min_value = 0, max_value = 100, value = 85)

if last_temp > min_temp and last_temp < max_temp:
    temp_msg = f'ℹ️ - El valor de temperatura es normal: {last_temp}ºC'
    st.info(temp_msg)
else:
    temp_msg = f"❗ - El valor de temperatura se sale de los rangos establecidos: {last_temp}ºC"
    st.info(temp_msg)

if last_hum > min_hum and last_hum < max_hum:
    hum_msg = f'ℹ️ - El valor de humedad es normal: {last_hum}%'
    st.info(hum_msg)
else:
    hum_msg = f"❗ - El valor de humedad se sale de los rangos establecidos: {last_hum}%" 
    st.info(hum_msg)

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
token_dict = {
    "token": st.secrets["token"], 
    "refresh_token": st.secrets["refresh_token"], 
    "token_uri": st.secrets["token_uri"], 
    "client_id": st.secrets["client_id"], 
    "client_secret": st.secrets["client_secret"], 
    "scopes": st.secrets["scopes"], 
    "expiry": st.secrets["expiry"]
}
creds = Credentials.from_authorized_user_info(token_dict, SCOPES)
message = MIMEMultipart()
message['subject'] = 'Alerta!: Valores fuera de rango'
message.attach(MIMEText(f'{temp_msg}\n{hum_msg}\n\nDesafío 2 - Desarrollo de Proyectos y Productos de Datos', 'plain'))

dest = st.text_input(label = "Ingrese su mail:")
message['to'] = dest

if st.button(label = "Enviar alarma"):
    st.write("Alarma enviada al email")
    service = build('gmail', 'v1', credentials=creds)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    try:
        message = (service.users().messages().send(userId='me', body={'raw': raw_message}).execute())
        print(f'Correo electrónico enviado. ID del mensaje: {message["id"]}')
    except HttpError as error:
        print(f'Error al enviar el correo electrónico: {error}')