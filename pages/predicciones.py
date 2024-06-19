import streamlit as st
import pandas as pd 
from pycaret.classification import *
from pycaret.time_series import load_model as load_ts_model, predict_model as predict_ts_model
import streamlit as st
import pandas as pd
from datetime import timedelta, date
import utils
import json 
import urllib.request
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import ssl

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

# Definir una función para cargar los datos
if 'df' not in st.session_state:
    st.error("El DataFrame no está inicializado. Asegúrate de inicializarlo en el archivo principal.")
else:
    df = st.session_state.df.copy()


#* --------------------Cargamos las variables de entorno ------------------#
load_dotenv()
ssl._create_default_https_context = ssl._create_stdlib_context
AZURE_ST_URL = os.getenv('AZURE_ST_URL')
AZURE_ST_API = os.getenv('AZURE_ST_API')
AZURE_CLAS_URL = os.getenv('AZURE_CLAS_URL')
AZURE_CLAS_API = os.getenv('AZURE_CLAS_API')


# Cargar modelo de clasificación
model = load_model('modelos/modelo_lesividad')

# Cargar modelo de series temporales
ts_model = load_ts_model('modelos/exp_smooth_model')

# Función para predecir lesividad usando PyCaret
def predict_lesividad_pycaret(input_data):
    prediction = predict_model(model, data=input_data).round(2)
    return prediction["prediction_label"][0]

# Función para predecir accidentes futuros usando PyCaret
def predict_future_accidents_pycaret(ts_model, period=90):
    future_predictions = predict_ts_model(ts_model, fh=period)
    return future_predictions['y_pred'].values.ravel().tolist()

# Función para predecir usando Azure
def predict_azure(url, api_key, data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + api_key)
    }
    body = str.encode(json.dumps(data))
    try:
        req = urllib.request.Request(url, body, headers)
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf8", 'ignore'))
            return int(result[0])
    except urllib.error.HTTPError as error:
        st.error(f'Error al realizar la predicción. Código de error HTTP: {error.code}')
        st.error(f'Información adicional: {error.info()}')
        st.error(f'Detalle del error: {error.read().decode("utf8", "ignore")}')
        return None

# Menú lateral
utils.menu()

# Predicción de accidentes
st.title("Accidentes posibles:")
future_date = st.date_input("Seleccione una fecha:", min_value=date.today() + timedelta(days=1), max_value=date(2024, 7, 29))
days_to_future = (future_date - date.today()).days
if days_to_future < 1:
    st.warning("Por favor seleccione una fecha futura.")
else:
    if st.button('Realizar predicción'):
        st.write("Realizando la predicción... Esto puede tomar unos momentos.")
        future_accidents_pycaret = predict_future_accidents_pycaret(ts_model, period=min(days_to_future, 90))
        data = {
                "input_data": {
                    "columns": ["Fecha"],
                    "index": [0],
                    "data": [str(future_date)]
                }
            }
        azure_result = predict_azure(AZURE_ST_URL, AZURE_ST_API, data)
        
        col1, col2 = st.columns(2)
        with col1:
        # Predicción con PyCaret
        
            if future_accidents_pycaret is not None:
                st.write(f"Predicción de accidentes con pycaret: {round(future_accidents_pycaret[-1])}")

        with col2:
        # Predicción con Azure
            if azure_result is not None:
                st.write("Predicción de accidentes con Azure:", str(azure_result))


# Predicción de lesividad
st.title("Seleccione los factores para predecir la lesividad:")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='color: blue;'>Factor Medio Ambiente</h3>", unsafe_allow_html=True)
    Estado_meteorológico = st.selectbox('Estado meteorológico', options=['Seleccione una opción'] + list(df['Estado meteorológico'].unique()))
    Tipo_vía = st.selectbox('Tipo de vía', options=['Seleccione una opción'] + list(df['Tipo de vía'].unique()))

with col2:
    st.markdown("<h3 style='color: blue;'>Factor Humano</h3>", unsafe_allow_html=True)
    Edad = st.slider('Edad del implicado', min_value=18, max_value=100, value=30, step=1)
    Sexo = st.selectbox('Sexo', options=['Seleccione una opción'] + list(df['Sexo'].unique()))
    Implicado = st.selectbox('Implicado', options=['Seleccione una opción'] + list(df['Implicado'].unique()))
    Positivo_alcohol = st.selectbox('Positivo alcohol', options=['Seleccione una opción'] + list(df['Positivo alcohol'].unique()))
    Positivo_droga = st.selectbox('Positivo droga', options=['Seleccione una opción'] + list(df['Positivo droga'].unique()))

with col3:
    st.markdown("<h3 style='color: blue;'>Otros Factores</h3>", unsafe_allow_html=True)
    Distrito = st.selectbox('Distrito', options=['Seleccione una opción'] + list(df['Distrito'].unique()))
    Día_semana = st.selectbox('Día semana', options=['Seleccione una opción'] + list(df['Día semana'].unique()))
    Horario = st.selectbox('Tramo horario', options=['Seleccione una opción'] + list(df['Tramo horario'].unique()))
    Tipo_vehiculo = st.selectbox('Tipo vehiculo', options=['Seleccione una opción'] + list(df['Tipo vehiculo'].unique()))


if st.button('Predecir Lesividad con PyCaret'):
    st.write("Realizando la predicción... Esto puede tomar unos momentos.")

    col1, col2 = st.columns(2)
    with col1:


            input_data = pd.DataFrame({
                'Expediente': [0],
                'Fecha': [''],
                'Tipo día': [0],
                'Hora': [0],
                'Tipo de vía': [Tipo_vía if Tipo_vía != 'Seleccione una opción' else 'Desconocido'],
                'Calle': [''],
                'Latitud': [0.0],
                'Longitud': [0.0],
                'Tipo accidente': [''],
                'Positivo alcohol': [Positivo_alcohol if Positivo_alcohol != 'Seleccione una opción' else 'Desconocido'],
                'Positivo droga': [Positivo_droga if Positivo_droga != 'Seleccione una opción' else 'Desconocido'],
                'Distrito': [Distrito if Distrito != 'Seleccione una opción' else 'Desconocido'],
                'Tipo vehiculo': [Tipo_vehiculo if Tipo_vehiculo != 'Seleccione una opción' else 'Desconocido'],
                'Día semana': [Día_semana if Día_semana != 'Seleccione una opción' else 'Desconocido'],
                'Sexo': [Sexo if Sexo != 'Seleccione una opción' else 'Desconocido'],
                'Edad': [Edad],
                'Tramo horario': [Horario if Horario != 'Seleccione una opción' else 'Desconocido'],
                'Estado meteorológico': [Estado_meteorológico if Estado_meteorológico != 'Seleccione una opción' else 'Desconocido'],
                'Implicado': [Implicado if Implicado != 'Seleccione una opción' else 'Desconocido'],
            })
            prediction_pycaret = predict_lesividad_pycaret(input_data)
            st.write(f'La lesividad podría ser {prediction_pycaret}')

    with col2:
            data = {
                "input_data": {
                    "columns": [
                        "Día semana", "Tipo día", "Tramo horario", "Distrito", "Tipo de vía", "Tipo accidente",
                        "Estado meteorológico", "Tipo vehiculo", "Implicado", "Sexo", "Edad", "Positivo alcohol", "Positivo droga"
                    ],
                    "index": [0],
                    "data": [[
                        Día_semana if Día_semana != 'Seleccione una opción' else '',
                        '',  # Tipo día
                        Horario if Horario != 'Seleccione una opción' else '',
                        Distrito if Distrito != 'Seleccione una opción' else '',
                        Tipo_vía if Tipo_vía != 'Seleccione una opción' else '',
                        '',  # Tipo accidente
                        Estado_meteorológico if Estado_meteorológico != 'Seleccione una opción' else '',
                        Tipo_vehiculo if Tipo_vehiculo != 'Seleccione una opción' else '',
                        Implicado if Implicado != 'Seleccione una opción' else '',
                        Sexo if Sexo != 'Seleccione una opción' else '',
                        Edad,
                        Positivo_alcohol if Positivo_alcohol != 'Seleccione una opción' else '',
                        Positivo_droga if Positivo_droga != 'Seleccione una opción' else ''
                    ]]
                }
            }
            azure_result_lesividad = predict_azure(AZURE_CLAS_URL, AZURE_CLAS_API, data)
            if azure_result_lesividad is not None:
                st.write("Resultado de la predicción de lesividad con Azure:", azure_result_lesividad)
