import streamlit as st
import pandas as pd 
from pycaret.classification import *
from pycaret.time_series import load_model as load_ts_model, predict_model as predict_ts_model
import streamlit as st
import pandas as pd
from datetime import timedelta, date
import utils
from dotenv import load_dotenv
import os
import ssl
import json 
import urllib.request

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

#* -------------------- Sidebar  ------------------#
utils.menu()

#* --------------------Cargamos las variables de entorno ------------------#
ssl._create_default_https_context = ssl._create_stdlib_context # Se crea un contexto SSL para realizar la solicitud a la API
load_dotenv()
accidentes_url= os.getenv('ACCIDENTES_URL')
accidentes_api = os.getenv('ACCIDENTES_API')
lesividad_url= os.getenv('LESIVIDAD_URL')
lesividad_api = os.getenv('LESIVIDAD_API')


#* --------------------Generamos mapeo de Valores Booleanos ------------------#
alcohol_map = {0: 'No', 1: 'Si'}
inverse_alcohol_map = {v: k for k, v in alcohol_map.items()}
droga_map = {0.0: 'No', 1.0: 'Si'}
inverse_droga_map = {v: k for k, v in droga_map.items()}

# Definir una función para cargar los datos
if 'df' in st.session_state :
    df = st.session_state.df.copy()

    # Cargar modelo de clasificación

    #? -------------------- Pycaret Lesividad : Clasificación ----------------#
    def lesividad_pycaret(input_data):
        model = load_model('modelos/modelo_lesividad')

        prediction = predict_model(model, data=input_data).round(2)  # Realizar la predicción
        return prediction["prediction_label"][0]  # Devolver la predicción

    #? -------------------- Pycaret Accidentes : Serie Temporal ----------------#
    def accidentes_pycaret(period=90):
        ts_model = load_ts_model('modelos/exp_smooth_model')
        future_predictions = predict_ts_model(ts_model, fh=period)  # Realizar la predicción
        return future_predictions['y_pred'].values.ravel().tolist()  # Devolver las predicciones

    #? -------------------- Azure Accidentes : Serie Temporal ----------------#
    def accidentes_azure(fecha):
        data = {"input_data": {
        "columns":["Fecha"],
        "index":[0],
        "data":[str(fecha)]
        }
        }
        body = str.encode(json.dumps(data))
        headers = {
                'Content-Type': 'application/json',
                'Authorization': ('Bearer ' + accidentes_api)
            }
        try:
            req = urllib.request.Request(accidentes_url, body, headers)

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf8", 'ignore'))                   
            return int(result[0])
        except urllib.error.HTTPError as error:
            return f'Error en la solicitud a la API de Azure {str(error.code)} - {error.info()} '
        
    #? -------------------- Azure Lesividad : Clasificación ----------------#
    def lesividad_azure(input_data):
        #Borramos las columnas que no se necesitan
        input_data.drop(columns=['Expediente', 'Fecha', 'Hora', 'Calle', 'Latitud', 'Longitud'], inplace=True)
        input_data = input_data.reindex(columns=['Día semana','Tipo día','Tramo horario','Distrito','Tipo de vía','Tipo accidente','Estado meteorológico','Tipo vehiculo','Implicado','Sexo','Edad','Positivo alcohol','Positivo droga'])
        data = {
            "input_data": {
                "columns": list(input_data.columns),
                "index": list(input_data.index),
                "data": input_data.to_dict('records')
                }
            }
        data = {
            "input_data": {
                "columns": list(input_data.columns),
                "index": list(input_data.index),
                "data": input_data.to_dict('records')
            }
        }
        body = json.dumps(data).encode('utf-8')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + lesividad_api
        }

        try:
            req = urllib.request.Request(lesividad_url, body, headers)
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf8", 'ignore'))
                return result[0]
        except urllib.error.HTTPError as error:
            return f'Error en la solicitud a la API de Azure {str(error.code)} - {error.info()} '
    # Título de la predicción de accidentes
    st.subheader("Accidentes posibles:")
    # Elementos interactivos para la predicción de accidentes
    future_date = st.date_input("Seleccione una fecha:", min_value=date.today()+timedelta(days=1), max_value=date(2024, 7, 29)) # Seleccionar una fecha futura
    days_to_future = (future_date - date.today()).days # Calcular los días hasta la fecha futura
    if days_to_future < 1: # Si la fecha seleccionada ya pasó
        st.warning("Por favor seleccione una fecha futura.")
    else:
        fecha , pycaret, azure = st.columns(3) # Crear columnas para los botones de predicción
        with fecha:
            st.write(f'Fecha seleccionada: {future_date.strftime("%Y-%m-%d")}')
        with pycaret:
            future_accidents = accidentes_pycaret(period=min(days_to_future, 90)) # Realizar la predicción de accidentes
            st.write(f'Nº Accidentes predichos por Pycaret es de: {round(future_accidents[-1])}') # Mostrar la última predicción
        with azure: 
            azure_result = accidentes_azure(future_date)
            st.write("Nº Accidentes predichos por Azure es de :", str(azure_result))

        # Título de la predicción de lesividad
        st.subheader("Seleccione los factores para predecir la lesividad:")

        # Elementos interactivos para la predicción de lesividad
        factorZona, factorHumano, factorOtros = st.columns(3)
        calcular_lesividad = False
        with factorZona:
            st.markdown("<h5 style='color: blue;'>Factor Zona</h5>", unsafe_allow_html=True)
            Distrito = st.selectbox('Distrito', options=['Seleccione una opción'] + list(df['Distrito'].unique()))
            Tipo_vía = st.selectbox('Tipo de vía', options=['Seleccione una opción'] + list(df['Tipo de vía'].unique()))
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)  # Añade saltos de línea
            
            if st.button('Predecir Lesividad'):
                    calcular_lesividad = True


        with factorHumano:
            st.markdown("<h5 style='color: blue;'>Factor Humano</h5>", unsafe_allow_html=True)
            Sexo = st.selectbox('Sexo', options=['Seleccione una opción'] + list(df['Sexo'].unique()))
            col1, col2 = st.columns(2)
            with col1:
                Implicado = st.selectbox('Implicado', options=['Seleccione una opción'] + list(df['Implicado'].unique()))
                selected_alcohol = st.selectbox('Positivo alcohol', options=['Seleccione una opción'] + [alcohol_map[val] for val in df['Positivo alcohol'].unique()])
                if selected_alcohol != 'Seleccione una opción':
                    selected_alcohol_value = inverse_alcohol_map[selected_alcohol]
            with col2:
                Tipo_vehiculo = st.selectbox('Tipo vehiculo', options=['Seleccione una opción'] + list(df['Tipo vehiculo'].unique()))
                selected_droga = st.selectbox('Positivo droga', options=['Seleccione una opción'] + [droga_map[val] for val in df['Positivo droga'].unique()])
                if selected_droga != 'Seleccione una opción':
                    selected_droga_value = inverse_droga_map[selected_droga]
            Edad = st.slider('Edad del implicado', min_value=18, max_value=100, value=30, step=1)

        with factorOtros:

            st.markdown("<h5 style='color: blue;'>Otros Factores</h5>", unsafe_allow_html=True)
            Tipo_Accidente = st.selectbox('Tipo Accidentes', options=['Seleccione una opción'] + list(df['Tipo accidente'].unique()))
            col1, col2 = st.columns(2)
            with col1:
                Tipo_día = st.selectbox('Tipo día', options=['Seleccione una opción'] + list(df['Tipo día'].unique()))
                Horario = st.selectbox('Tramo horario', options=['Seleccione una opción'] + list(df['Tramo horario'].unique()))
            with col2:
                Día_semana = st.selectbox('Día semana', options=['Seleccione una opción'] + list(df['Día semana'].unique()))
                Estado_meteorológico = st.selectbox('Estado meteorológico', options=['Seleccione una opción'] + list(df['Estado meteorológico'].unique()))
                
        if  calcular_lesividad==True:
            datos , pycarte , azure = st.columns(3)
            # Mostrar mensaje de espera
            with st.spinner('Realizando la predicción de Lesividad.......'):
                # Realizar la predicción
                input_data = pd.DataFrame({ # Crear un DataFrame con los datos de entrada
                    'Expediente': [0],
                    'Fecha': [''],
                    'Tipo día': [0],
                    'Hora': [0],
                    'Tipo de vía': [Tipo_vía if Tipo_vía != 'Seleccione una opción' else 'Desconocido'],
                    'Calle': [''],
                    'Latitud': [0.0],
                    'Longitud': [0.0],
                    'Tipo accidente': [''],
                    'Positivo alcohol': [0],
                    'Positivo droga': [0],
                    'Distrito': [Distrito if Distrito != 'Seleccione una opción' else 'Desconocido'],
                    'Tipo vehiculo': [Tipo_vehiculo if Tipo_vehiculo != 'Seleccione una opción' else 'Desconocido'],
                    'Día semana': [Día_semana if Día_semana != 'Seleccione una opción' else 'Desconocido'],
                    'Sexo': [Sexo if Sexo != 'Seleccione una opción' else 'Desconocido'],
                    'Edad': [Edad],
                    'Tramo horario': [Horario if Horario != 'Seleccione una opción' else 'Desconocido'],
                    'Estado meteorológico': [Estado_meteorológico if Estado_meteorológico != 'Seleccione una opción' else 'Desconocido'],
                    'Implicado': [Implicado if Implicado != 'Seleccione una opción' else 'Desconocido'],
                })
                with datos:
                    st.write()
                with pycarte:
                    prediction = lesividad_pycaret(input_data) # Realizar la predicción
                    st.write(f'Lesividad predicha por Pycaret es {prediction}')
                with azure:
                    prediction = lesividad_azure(input_data) # Realizar la predicción
                    st.write(f'Lesividad predicha por Azure es {prediction}')


