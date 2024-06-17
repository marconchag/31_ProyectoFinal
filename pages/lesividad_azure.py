import streamlit as st
import urllib.request
import json 
import ssl 
import utils
from dotenv import load_dotenv
import os


#------------------Cargar Datos----------------------#
# Definir una función para cargar los datos
if 'df' not in st.session_state:
    st.error("El DataFrame no está inicializado. Asegúrate de inicializarlo en el archivo principal.")
else:
    df = st.session_state.df.copy()
 
if 'df_agrupado' not in st.session_state:
    st.error("El DataFrame no está inicializado. Asegúrate de inicializarlo en el archivo principal.")
else:
    df_agrupado = st.session_state.df_agrupado.copy()


utils.menu()



#* --------------------Cargamos las variables de entorno ------------------#
load_dotenv()
ssl._create_default_https_context = ssl._create_stdlib_context # Se crea un contexto SSL para realizar la solicitud a la API
URL = os.getenv('AZURE_CLAS_URL')
API = os.getenv('AZURE_CLAS_API')


st.title('Predicción de Lesividad de Accidentes en Madrid')

# Obtener valores únicos para los selectores
dias_semana = df['Día semana'].unique().tolist() # Se obtienen los valores únicos de la columna 'Día semana' y se convierten en una lista
tipos_dia = df['Tipo día'].unique().tolist()
tramos_horarios = df['Tramo horario'].unique().tolist()
distritos = df['Distrito'].unique().tolist()
tipos_via = df['Tipo de vía'].unique().tolist()
tipos_accidente = df['Tipo accidente'].unique().tolist()
estados_meteorologicos = df['Estado meteorológico'].unique().tolist()
tipos_vehiculo = df['Tipo vehiculo'].unique().tolist()
implicados = df['Implicado'].unique().tolist()
sexos = df['Sexo'].unique().tolist()
edades = df['Edad'].unique().tolist()
positivos_alcohol = df['Positivo alcohol'].unique().tolist()
positivos_droga = df['Positivo droga'].unique().tolist()

# Crear los selectores usando los valores únicos
dia_semana = st.selectbox('Día de la semana', ['(Opcional)'] + dias_semana) # Se añade la opción '(Opcional)' al principio de la lista luego se añaden los valores únicos
tipo_dia = st.selectbox('Tipo de día', ['(Opcional)'] + tipos_dia)
tramo_horario = st.selectbox('Tramo horario', ['(Opcional)'] + tramos_horarios)
distrito = st.selectbox('Distrito', ['(Opcional)'] + distritos)
tipo_via = st.selectbox('Tipo de vía', ['(Opcional)'] + tipos_via)
tipo_accidente = st.selectbox('Tipo de accidente', ['(Opcional)'] + tipos_accidente)
estado_meteorologico = st.selectbox('Estado meteorológico', ['(Opcional)'] + estados_meteorologicos)
tipo_vehiculo = st.selectbox('Tipo de vehículo', ['(Opcional)'] + tipos_vehiculo)
implicado = st.selectbox('Implicado', ['(Opcional)'] + implicados)
sexo = st.selectbox('Sexo', ['(Opcional)'] + sexos) 
edad = st.selectbox('Edad', ['(Opcional)'] + edades)
positivo_alcohol = st.selectbox('Positivo en alcohol', ['(Opcional)'] + [0, 1])
positivo_droga = st.selectbox('Positivo en droga', ['(Opcional)'] + [0, 1])


# Realizar la predicción al presionar el botón
if st.button('Realizar predicción'):
    # Verificar que al menos un campo no esté en '(Opcional)'
    if (dia_semana == '(Opcional)' and tipo_dia == '(Opcional)' and tramo_horario == '(Opcional)' and
        distrito == '(Opcional)' and tipo_via == '(Opcional)' and tipo_accidente == '(Opcional)' and
        estado_meteorologico == '(Opcional)' and tipo_vehiculo == '(Opcional)' and implicado == '(Opcional)' and
        sexo == '(Opcional)' and edad == '(Opcional)' and positivo_alcohol == '(Opcional)' and positivo_droga == '(Opcional)'):
        st.error("Por favor, selecciona al menos un campo para realizar la predicción.")
    else:
        data = {
            "input_data": {
                "columns": [
                    "Día semana",
                    "Tipo día",
                    "Tramo horario",
                    "Distrito",
                    "Tipo de vía",
                    "Tipo accidente",
                    "Estado meteorológico",
                    "Tipo vehiculo",
                    "Implicado",
                    "Sexo",
                    "Edad",
                    "Positivo alcohol",
                    "Positivo droga"
                ],
                "index": [0],
                "data": [[
                    dia_semana if dia_semana != '(Opcional)' else '',
                    tipo_dia if tipo_dia != '(Opcional)' else '',
                    tramo_horario if tramo_horario != '(Opcional)' else '',
                    distrito if distrito != '(Opcional)' else '',
                    tipo_via if tipo_via != '(Opcional)' else '',
                    tipo_accidente if tipo_accidente != '(Opcional)' else '',
                    estado_meteorologico if estado_meteorologico != '(Opcional)' else '',
                    tipo_vehiculo if tipo_vehiculo != '(Opcional)' else '',
                    implicado if implicado != '(Opcional)' else '',
                    sexo if sexo != '(Opcional)' else '',
                    edad if edad != '(Opcional)' else '',
                    positivo_alcohol if positivo_alcohol != '(Opcional)' else 0,
                    positivo_droga if positivo_droga != '(Opcional)' else 0
                ]]
            }
        }



#SI QUIEREN ELEGIR TODAS LAS OPCIONES Y QUE NO SEAN OPCIONALES DESCOMENTAR ÉSTO Y ELIMINAR EL CODIGO DE ARRIBA, SI NO ELIMINAR COMENTARIO

# # Obtener valores únicos para los selectores
# dias_semana = df['Día semana'].unique().tolist()
# tipos_dia = df['Tipo día'].unique().tolist()
# tramos_horarios = df['Tramo horario'].unique().tolist()
# distritos = df['Distrito'].unique().tolist()
# tipos_via = df['Tipo de vía'].unique().tolist()
# tipos_accidente = df['Tipo accidente'].unique().tolist()
# estados_meteorologicos = df['Estado meteorológico'].unique().tolist()
# tipos_vehiculo = df['Tipo vehiculo'].unique().tolist()
# implicados = df['Implicado'].unique().tolist()
# sexos = df['Sexo'].unique().tolist()
# edades = df['Edad'].unique().tolist()
# positivos_alcohol = df['Positivo alcohol'].unique().tolist()
# positivos_droga = df['Positivo droga'].unique().tolist()

# # Crear los selectores usando los valores únicos
# dia_semana = st.selectbox('Día de la semana', dias_semana)
# tipo_dia = st.selectbox('Tipo de día', tipos_dia)
# tramo_horario = st.selectbox('Tramo horario', tramos_horarios)
# distrito = st.selectbox('Distrito', distritos)
# tipo_via = st.selectbox('Tipo de vía', tipos_via)
# tipo_accidente = st.selectbox('Tipo de accidente', tipos_accidente)
# estado_meteorologico = st.selectbox('Estado meteorológico', estados_meteorologicos)
# tipo_vehiculo = st.selectbox('Tipo de vehículo', tipos_vehiculo)
# implicado = st.selectbox('Implicado', implicados)
# sexo = st.selectbox('Sexo', sexos)
# edad = st.selectbox('Edad', edades)
# positivo_alcohol = st.selectbox('Positivo en alcohol', positivos_alcohol)
# positivo_droga = st.selectbox('Positivo en droga', positivos_droga)

# # Realizar la predicción al presionar el botón
# if st.button('Realizar predicción'):
#     data = {
#         "input_data": {
#             "columns": [
#                 "Día semana",
#                 "Tipo día",
#                 "Tramo horario",
#                 "Distrito",
#                 "Tipo de vía",
#                 "Tipo accidente",
#                 "Estado meteorológico",
#                 "Tipo vehiculo",
#                 "Implicado",
#                 "Sexo",
#                 "Edad",
#                 "Positivo alcohol",
#                 "Positivo droga"
#             ],
#             "index": [0],
#             "data": [[
#                 dia_semana,
#                 tipo_dia,
#                 tramo_horario,
#                 distrito,
#                 tipo_via,
#                 tipo_accidente,
#                 estado_meteorologico,
#                 tipo_vehiculo,
#                 implicado,
#                 sexo,
#                 edad,
#                 positivo_alcohol,
#                 positivo_droga
#             ]]
#         }
#     }

    # Preparar y enviar la solicitud
    body = json.dumps(data).encode('utf-8') # Se codifica el diccionario en formato JSON
    headers = { # Se definen los encabezados de la solicitud
        'Content-Type': 'application/json', # Se especifica que el contenido es JSON
        'Authorization': 'Bearer ' + API # Se añade el token de autorización
    }

    try: # Se realiza la solicitud a la API
        req = urllib.request.Request(URL, body, headers) # Se crea la solicitud con la URL, el cuerpo y los encabezados
        with urllib.request.urlopen(req) as response: # Se abre la conexión y se obtiene la respuesta
            result = json.loads(response.read().decode("utf8", 'ignore')) # Se decodifica la respuesta y se convierte en un diccionario
            # Acceder al resultado de la predicción
            st.write("Resultado de la predicción:", result[0]) # Se muestra el resultado de la predicción
    except urllib.error.HTTPError as error: # Se maneja el error en caso de que la solicitud falle
        st.error(f'Error al realizar la predicción. Código de error HTTP: {error.code}') # Se muestra un mensaje de error con el código de error HTTP
        st.error(f'Información adicional: {error.info()}') # Se muestra información adicional del error
        st.error(f'Detalle del error: {error.read().decode("utf8", "ignore")}') # Se muestra el detalle del error