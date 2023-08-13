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
message['subject'] = 'Cambio en los valores esperados'
message.attach(MIMEText('Correo electrónico de prueba para Desafío producto de datos.', 'plain'))

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