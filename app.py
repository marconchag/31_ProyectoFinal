# -------------------IMPORTACIONES----------------------#
import streamlit as st
# Importamos componentes
import utils
import estilos
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS   
import locale
import numpy as np
from PIL import Image
import calendar

pio.templates.default = "plotly_dark"
# Establecer la localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
pd.set_option('display.max_columns', None) 

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

#------------------Cargar Datos----------------------#
# Con el decorador cache_data solo cargamos los datos la primera vez que se carga la página
@st.cache_data (show_spinner="Cargando Datos...")  # 👈 Add the caching decorator
def load_data(url):
        df = pd.read_csv(url)
        return df

st.session_state.df = load_data(r'datos_procesados/accidentes_procesados.csv')
st.session_state.df_agrupado= load_data(r'datos_procesados/accidentes_procesados_agrupados.csv')
df = st.session_state.df.copy()

#------------------- Título de la página -------------------#
st.title('Accidentes de tráfico de la Comunidad de Madrid')

# --------------------SIDEBAR----------------------------#
utils.menu() #llamamos al menu

df = utils.filtros(['Sexo', 'Distrito'],df) #llamamos a los filtros

# Sección desplegable para la conclusión
with st.expander("Resumen", expanded=True):
    st.write("""
        El proyecto ha investigado varios factores influyentes en accidentes de tráfico en Madrid. 
        Utilizando estos datos, se ha desarrollado un modelo analítico y predictivo que ajusta los precios de seguros. 
        Este modelo emplea técnicas avanzadas de análisis de datos y aprendizaje automático para evaluar riesgos como el perfil del 
        conductor, tipo de vehículo, condiciones meteorológicas, características de la vía y horarios. El resultado es un prototipo
        web interactivo que calcula la probabilidad y gravedad de accidentes. Esto permite ajustes 
        equitativos en las tarifas de seguros y promueve estrategias más efectivas de prevención de accidentes.
    """)

    # Convertir la columna 'Fecha' al formato de Fecha adecuado
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Excluir el año 2024 y calcular el año con menos accidentes
    accidentes_por_año = df[df['Fecha'].dt.year < 2024].groupby(df['Fecha'].dt.year)['Expediente'].nunique()
    año_con_menos_accidentes = accidentes_por_año.idxmin()

    # Calcular el mes con menos accidentes
    accidentes_por_mes = df.groupby(df['Fecha'].dt.month)['Expediente'].nunique()
    mes_con_menos_accidentes = accidentes_por_mes.idxmin()

    # Convertir el número del mes a nombre
    mes_con_menos_accidentes_nombre = calendar.month_name[mes_con_menos_accidentes]

    # Tipo de accidente predominante
    tipo_accidente_predominante = df['Tipo accidente'].mode()[0]

    # Distrito con más accidentes
    distrito_con_mas_accidentes = df['Distrito'].value_counts().idxmax()

    # Vehículo más involucrado
    vehiculo_mas_involucrado = df['Tipo vehiculo'].mode()[0]

    # Horario pico de accidentes
    horario_pico_accidentes = df['Tramo horario'].mode()[0]

    # Accidentes por género
    accidentes_por_genero = df['Sexo'].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    porcentaje_hombres = accidentes_por_genero['Hombre']

    # Días con más accidentes
    dias_mas_accidentes = df['Tipo día'].mode()[0]

    # Gravedad de los accidentes
    gravedad_predominante = df['Lesividad'].mode()[0]

    # Grupo de edad más afectado
    grupo_edad_mas_afectado = df['Edad'].value_counts().idxmax()

    # Porcentaje implicados fallecidos
        # Filtrar los registros donde hubo fallecidos
    fallecidos_df = df[df['Lesividad'] == 'Fallecido']
        # Obtener la distribución de fallecidos por tipo de implicado
    fallecidos_por_tipo = fallecidos_df['Implicado'].value_counts(normalize=True) * 100
        # Obtener el porcentaje de la categoría con más fallecimientos
    porcentaje_mas_implicados = fallecidos_por_tipo.max().round(1)


    # Porcentaje de fallecidos respecto al total de accidentes
    total_accidentes = len(df)
    total_fallecidos = len(df[df['Lesividad'] == 'Fallecido'])
    porcentaje_fallecidos_total = (total_fallecidos / total_accidentes) * 100

    datos_tarjetas = {
        "Año con menos accidentes": año_con_menos_accidentes,
        "Mes con Menos Accidentes": mes_con_menos_accidentes_nombre,
        "Accidente Predominante": tipo_accidente_predominante,
        "Distrito con más Accidentes": distrito_con_mas_accidentes,
        "Vehículo más Involucrado": vehiculo_mas_involucrado,
        "Horario pico de Accidentes": horario_pico_accidentes,
        "Accidentes por Género": porcentaje_hombres,
        "Días con más Accidentes": dias_mas_accidentes,
        "Gravedad de los Accidentes": gravedad_predominante,
        "Grupo Edad más Afectada": grupo_edad_mas_afectado,
        "Porcentaje de Fallecidos": f"{porcentaje_fallecidos_total:.2f}%",
        "Distribución de Fallecidos": f"{porcentaje_mas_implicados}% {fallecidos_por_tipo.idxmax()}"
    }

    # Generar tarjetas utilizando la función definida en estilos.py

    st.markdown(estilos.generar_tarjetas(datos_tarjetas), unsafe_allow_html=True)

#-------------------------- Grafico por años y meses ---------------------------#
#mostrar grafico de accidentes por años y meses separados
copia = df.copy()
# Convertir la columna 'fecha' al formato de fecha adecuado
copia['Fecha'] = pd.to_datetime(copia['Fecha'])

# Establecer la columna 'fecha' como índice del DataFrame
copia = copia.set_index('Fecha')

# Obtener el año actual
año_actual = pd.Timestamp.now().year

# Determinar cuántas filas y columnas necesitas para tus subgráficos
num_filas = (año_actual - copia.index.min().year + 1) // 3 + ((año_actual - copia.index.min().year + 1) % 2)
num_columnas = 3

# Lista para almacenar los datos de todos los años
datos_por_año = []

# Crear gráficos separados para cada año y calcular el rango máximo y mínimo de los datos
for i, año in enumerate(range(copia.index.min().year, año_actual + 1)):
    # Filtrar el DataFrame para el año actual
    copia_año = copia[copia.index.year == año]
    
    # Agrupar por mes y contar las ocurrencias
    total_por_mes = copia_año.resample('M')['Expediente'].nunique().reset_index(name='cantidad')
    
    # Agregar los datos de este año a la lista
    datos_por_año.append(total_por_mes['cantidad'])
    
# Calcular el rango máximo y mínimo de todos los datos
y_min = min([min(datos) for datos in datos_por_año])
y_max = max([max(datos) for datos in datos_por_año])

# Crear una figura con subplots
fig4 = make_subplots(rows=num_filas, cols=num_columnas, subplot_titles=[f'Año {año}' for año in range(copia.index.min().year, año_actual + 1)],
                    vertical_spacing=0.15)

# Definir una paleta de colores
palette = px.colors.sequential.Viridis

# Crear gráficos separados para cada año y agregarlos a las subtramas
for i, año in enumerate(range(copia.index.min().year, año_actual + 1)):
    # Filtrar el DataFrame para el año actual
    copia_año = copia[copia.index.year == año]
    
    # Agrupar por mes y contar las ocurrencias
    total_por_mes = copia_año.resample('M')['Expediente'].nunique().reset_index(name='cantidad')
    
    # Obtener el nombre del mes en español
    total_por_mes['mes'] = total_por_mes['Fecha'].dt.strftime('%B')
    
    # Seleccionar un color de la paleta para este año
    color = palette[i % len(palette)]
    
    # Calcular la fila y columna para esta subtrama
    fila = i // num_columnas + 1
    columna = i % num_columnas + 1
    
    # Agregar el gráfico a la subtrama correspondiente
    fig4.add_trace(
        go.Scatter(x=total_por_mes['mes'], y=total_por_mes['cantidad'], name=f'Año {año}', line=dict(color=color)),
        row=fila,
        col=columna)

# Establecer el mismo rango en el eje y para todos los subgráficos
fig4.update_yaxes(range=[y_min, y_max])

# Actualizar el diseño de las subtramas
fig4.update_layout(height=1000, width=1300, showlegend=False, title='Accidentes por mes en cada año')

# Mostrar la figura
st.plotly_chart(fig4, use_container_width=True)

#--------------------CONTENIDO---------------------------#
# Aplicar estilos CSS personalizados
estilos.pestañas()

# Crear pestañas
tab1, tab2 = st.tabs(["Tipo de vía", "Distritos"])

# Contenido de la pestaña Vehículos
#TAB 6: TIPO DE VIA
with tab1:

    col1, col2 = st.columns(2)
#nube de palabras
#mostrar la nube de palabras en streamlit
    with col1:
        # Cargar la imagen de la máscara
        mascara = np.array(Image.open("img//mapa_madrid.jpg"))

        # Suponiendo que tienes una columna 'nombre_calle_cercana' en tu DataFrame de accidentes
        # Puedes usar value_counts() para contar la frecuencia de las calles y luego convertirlo a un diccionario

        # Calcular la frecuencia de las calles
        frecuencia_calles = df['Calle'].value_counts()

        # Convertir la Serie de pandas a un diccionario
        calles_dict = frecuencia_calles.to_dict()

        # Crear el WordCloud con la máscara y configuraciones adicionales
        wordcloud = (WordCloud(background_color='white', mask=mascara, contour_color='steelblue', contour_width=2).generate_from_frequencies(calles_dict)).to_array()
        st.image(wordcloud)
    
    with col2: 
            #-------Gráfico2: tipo de accidente según el tipo de via ------#
        #nube de palabras
        
        # Cargar la imagen de la máscara
        mascara = np.array(Image.open("img//mapa_madrid.jpg"))

        # Suponiendo que tienes una columna 'nombre_calle_cercana' en tu DataFrame de accidentes
        # Puedes usar value_counts() para contar la frecuencia de las calles y luego convertirlo a un diccionario

        # Calcular la frecuencia de las calles
        frecuencia_calles = df['Tipo de vía'].value_counts()

        # Convertir la Serie de pandas a un diccionario
        calles_dict = frecuencia_calles.to_dict()

        # Crear el WordCloud con la máscara y configuraciones adicionales
        wordcloud2 = (WordCloud(background_color='white', mask=mascara, contour_color='steelblue', contour_width=2).generate_from_frequencies(calles_dict)).to_array()
        st.image(wordcloud2)


# Contenido de la pestaña Distritos
with tab2:
    st.subheader("Número de accidentes por Distrito")
    
    # Contar el número de accidentes por Distrito
    distrito_counts = st.session_state.df['Distrito'].value_counts()

    # Crear el gráfico de barras
    fig2 = px.bar(y=distrito_counts.index,
                x=distrito_counts.values,
                orientation='h',
                title='Frecuencia de accidentes por Distrito',
                color=distrito_counts.values,
                color_continuous_scale='Viridis',
                labels={'color': ''})

    fig2.update_layout(yaxis_title='Distrito',
                    xaxis_title='Número de accidentes',
                    yaxis={'categoryorder': 'total ascending'},
                    height=600)

    st.plotly_chart(fig2, use_container_width=True)

    
# --------------- MAPA DE ACCIDENTES POR DISTRITOS -----------------#
    st.subheader("Mapa de accidentes por distritos")
    
    # Crear un gráfico de dispersión en el mapa con colores por Distrito
    fig3 = px.scatter_mapbox(st.session_state.df, lat="Latitud", lon="Longitud", hover_name="Expediente",
                            color="Distrito", zoom=10, color_discrete_sequence=px.colors.qualitative.Plotly)

    # Personalizar la apariencia del mapa
    fig3.update_layout(mapbox_style="carto-positron", 
                    mapbox_zoom=10, 
                    mapbox_center = {"lat": 40.4167, "lon": -3.70325})
    fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig3, use_container_width=True)

#with open('accidentes_Distrito.html', 'r', encoding='utf-8') as file:
#   html_code = file.read()
#st.components.v1.html(html_code, width=800, height=600)

# Cargar el gráfico HTML
#with open("treemap.html", "r", encoding="utf-8") as file:
#   html_code = file.read()

# Mostrar el gráfico HTML en Streamlit
#st.components.v1.html(html_code, width=800, height=600)


