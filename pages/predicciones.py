import streamlit as st
import pandas as pd 
from pycaret.classification import *
from pycaret.time_series import load_model as load_ts_model, predict_model as predict_ts_model
import streamlit as st
import pandas as pd
from datetime import timedelta, date
import utils

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

# Definir una función para cargar los datos
if 'df' not in st.session_state:
    st.error("El DataFrame no está inicializado. Asegúrate de inicializarlo en el archivo principal.")
else:
    df = st.session_state.df.copy()



# Cargar modelo de clasificación
model = load_model('modelos/modelo_lesividad')

# Cargar modelo de series temporales
ts_model = load_ts_model('modelos/exp_smooth_model')

# Sidebar
utils.menu()  
# Función para predecir lesividad
def predict_lesividad(input_data):
    """Realiza la predicción de lesividad."""
    prediction = predict_model(model, data=input_data).round(2)  # Realizar la predicción
    return prediction["prediction_label"][0]  # Devolver la predicción

# Función para predecir accidentes futuros
def predict_future_accidents(ts_model, period=90):
    """Genera predicciones futuras de accidentes para los próximos 'period' días."""
    future_predictions = predict_ts_model(ts_model, fh=period)  # Realizar la predicción
    return future_predictions['y_pred'].values.ravel().tolist()  # Devolver las predicciones

# Título de la predicción de accidentes
st.title("Accidentes posibles:")

# Elementos interactivos para la predicción de accidentes

future_date = st.date_input("Seleccione una fecha:", min_value=date.today()+timedelta(days=1), max_value=date(2024, 7, 29)) # Seleccionar una fecha futura
days_to_future = (future_date - date.today()).days # Calcular los días hasta la fecha futura
if days_to_future < 1: # Si la fecha seleccionada ya pasó
    st.warning("Por favor seleccione una fecha futura.")
else:
    future_accidents = predict_future_accidents(ts_model, period=min(days_to_future, 90)) # Realizar la predicción de accidentes
    st.write("Predicción de accidentes para la fecha seleccionada:") # Mostrar la fecha seleccionada
    st.write(future_date.strftime("%Y-%m-%d"))  # Mostrar la fecha seleccionada
    st.write(f"Predicción de accidentes: {round(future_accidents[-1])}") # Mostrar la última predicción

    # Título de la predicción de lesividad
    st.title("Seleccione los factores para predecir la lesividad:")

    # Elementos interactivos para la predicción de lesividad
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
        Tipo_vehiculo = st.selectbox('Tipo vehiculo', options=['Seleccione una opción'] + list(df['Tipo vehiculo'].unique()))

    with col3:
        st.markdown("<h3 style='color: blue;'>Otros Factores</h3>", unsafe_allow_html=True)
        Distrito = st.selectbox('Distrito', options=['Seleccione una opción'] + list(df['Distrito'].unique()))
        Día_semana = st.selectbox('Día semana', options=['Seleccione una opción'] + list(df['Día semana'].unique()))
        Horario = st.selectbox('Tramo horario', options=['Seleccione una opción'] + list(df['Tramo horario'].unique()))

    if st.button('Predecir Lesividad'):
        # Mostrar mensaje de espera
        st.write("Realizando la predicción... Esto puede tomar unos momentos.")

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
        prediction = predict_lesividad(input_data) # Realizar la predicción

        # Mostrar el resultado de la predicción
        st.write(f'La lesividad podría ser {prediction}')
