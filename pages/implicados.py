import streamlit as st
# Importamos componentes
import utils
import estilos
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

# *------------------Cargar Datos----------------------#
if 'df' in st.session_state :
    df = st.session_state.df.copy()

    #* ------------------Asignamos el título de la página ------------------#

    st.title("Registro de Implicados")


    #* --------------------SIDEBAR ------------------#
    utils.menu() #   👈

    #* ------------------ Añadimos los filtros ----------------------------#
    df = utils.filtros(['Año','Sexo','Día semana','Distrito','Tipo vehiculo','Edad','Implicado','Tipo accidente'],df)


    #?--------------------  Tarjeta principal  ----------------------------#
    implicados = df.shape[0]
    estilos.tarjeta_horizontal(implicados, 'Número de implicados en accidentes') #   👈

    # Dividir la página en dos columnas
    col1, col2 = st.columns([6, 1])

    #?------------------- Gráfico distribución de implicados en los accidentes por mes y año ---------------#
    df['Fecha'] =pd.to_datetime(df['Fecha'])

    # Agrupar por año y mes y contar las filas
    total_por_año_mes = df.groupby([df['Fecha'].dt.year.rename('año'), 
                                    df['Fecha'].dt.month.rename('mes')]).size().reset_index(name='cantidad de implicados')
    #Convertir el número de mes en un objeto datetime
    total_por_año_mes['mes'] = pd.to_datetime(total_por_año_mes['mes'], format='%m').dt.strftime('%B')

    #Graficar utilizando Plotly Express
    fig = px.line(total_por_año_mes, x='mes', y='cantidad de implicados', color='año',
                title = 'Distribución de implicados en los Accidentes por Mes y Año', 
                color_discrete_sequence=px.colors.sequential.Viridis)

    #Ajustar tamaño grafico
    fig.update_layout(height=600, width=1100)

    #Ajustar tamaño de la fuentes
    fig.update_xaxes(tickfont=dict(size=18))
    fig.update_yaxes(tickfont=dict(size=18))
    fig.update_layout(title_font_size=24)
    fig.update_layout(legend_title_font_size=16)

    # Mostrar el gráfico en la primera columna
    col1.plotly_chart(fig, use_container_width=True)

    #?------------------- Mostramos las tarjetas por lesividad ---------------#

    lesividad_counts = df['Lesividad'].value_counts()

    col2.markdown(estilos.tarjeta(lesividad_counts),unsafe_allow_html=True)

    #? -------------------- Mostramos las pestañas ----------------------------#
    # Pestañas para diferentes gráficos
    st.markdown("##### Más información")
    edades, tpVehiculo, fallecidos, positivos = st.tabs(["Edades", "Tipo de vehículo", "Fallecidos", "Alcohol y Drogas"])
    # CSS en las pestañas
    estilos.pestañas()

    with edades:
        #? -------------------- Gráfico distribución por lesividad y grupo edad ----------------------------#
        # Agrupar por tipo de lesividad y grupo de edad y contar las ocurrencias
        total_por_Lesividad_y_edad = df[df['Lesividad'].isin(['Grave', 'Fallecido'])].groupby(['Lesividad', 'Edad']).size().reset_index(name='cantidad')

        # Crear gráfico de barras apiladas
        fig = px.bar(total_por_Lesividad_y_edad, x='Edad', y='cantidad', color='Lesividad',
                    title='Distribución de tipo de lesividad por grupo de edad',
                    labels={'Edad': 'Grupo de Edad', 'cantidad': 'Cantidad de Accidentes'},
                    barmode='stack', 
                    color_discrete_sequence=px.colors.sequential.Viridis)

        # Mostrar la figura
        st.plotly_chart(fig, use_container_width=True)

        #? -------------------- Gráfico distribución de edades por lesividad ----------------------------#

        # Definir el orden de los grupos de edad
        edad_order = ['0-17', '18-29', '30-39', '40-49', '50-59', '60-64', '65-69', '70-74', '+74']

        # Convertir la columna Edad a tipo categórico con el orden específico
        df['Edad'] = pd.Categorical(df['Edad'], categories=edad_order, ordered=True)

        # Crear el boxplot interactivo con Plotly Express
        fig = px.box(
            df, 
            x='Lesividad', 
            y='Edad', 
            color='Lesividad', 
            category_orders={'Edad': edad_order},
            title='Distribución de Edades según Tipo de Lesividad',
            labels={'Lesividad': 'Lesividad', 'Edad': 'Edad'},
            template='plotly_dark', 
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        # Actualizar el diseño del gráfico
        fig.update_layout(
            title_font_size=20,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            legend_title_font_size=14,
            legend=dict(font=dict(size=12)),
        )

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)    
    with tpVehiculo:
        #? -------------------- Gráfico distribución de accidentes por tipo de vehículo y género ----------------------------#
        # Agrupar por Sexo y tipo de vehículo
        grouped_Sexo_vehiculo = st.session_state.df.groupby(['Sexo', 'Tipo vehiculo']).size().reset_index(name='count').sort_values('count', ascending=False)

        # Crear figura combinada de barras y líneas
        fig = go.Figure()

        # Definir la paleta de colores en tonos de azul y verde
        paleta_colores = px.colors.sequential.Viridis

        # Añadir barras para accidentes por tipo de vehículo y género
        for i, Sexo in enumerate(grouped_Sexo_vehiculo['Sexo'].unique()):
            Sexo_df = grouped_Sexo_vehiculo[grouped_Sexo_vehiculo['Sexo'] == Sexo]
            fig.add_trace(go.Bar(
                x=Sexo_df['Tipo vehiculo'],
                y=Sexo_df['count'],
                name=f'{Sexo}',
                marker=dict(color=paleta_colores[i % len(paleta_colores)], line=dict(width=1)),
                text=Sexo_df['count'],
                textposition='auto'
            ))

        # Diseño del gráfico
        fig.update_layout(
            title='Distribución de accidentes por tipo de vehículo y género',
            xaxis_title='Tipo de vehículo',
            yaxis_title='Cantidad de accidentes',
            barmode='group',
            legend_title='Género y tipo de accidente',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False, gridcolor='white'),
            font=dict(family='Arial', size=12, color='white'),
            margin=dict(l=50, r=50, t=80, b=50),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)
    with fallecidos:
        #? -------------------- Gráfico distribución de accidentes por tipo de vehículo y género ----------------------------#
        # Filtrar el DataFrame para incluir solo las filas con tipo de lesividad "Fallecido"
        df_fallecidos = df[df['Lesividad'] == 'Fallecido']

        # Agrupar por tipo de lesividad y tipo de persona y contar las ocurrencias
        fallecidos_tpPersona = df_fallecidos.groupby(['Implicado']).size().reset_index(name='cantidad')
        fallecidos_Sexo = df_fallecidos.groupby(['Sexo']).size().reset_index(name='cantidad')
        
        # Usar una paleta de colores predefinida de Plotly
        paleta_colores = px.colors.sequential.Viridis
        
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])

        fig.add_trace(go.Pie(labels=fallecidos_tpPersona['Implicado'].values,
                            values=fallecidos_tpPersona['cantidad'].values,
                            name='', textinfo='label+percent+value', showlegend=False, hole=.3,
                            marker=dict(colors=paleta_colores)), 1, 1)  # hole para hacer el donut

        fig.add_trace(go.Pie(labels=fallecidos_Sexo['Sexo'].values,
                            values=fallecidos_Sexo['cantidad'].values,
                            name='', textinfo='label+percent', showlegend=False, hole=.3,
                            marker=dict(colors=paleta_colores)), 1, 2)
        # Diseño del gráfico
        fig.update_layout(
            title_text="Fallecidos en accidentes por Implicado y Sexo",
            legend=dict(font=dict(size=14)) # Tamaño de la fuente de la leyenda
        )

        # Mostrar la figura en Streamlit
        st.plotly_chart(fig, use_container_width=True)
    with positivos:
        #? ---------------- Mapa de Calor : Implicados positivos en Alcohol y Drogas  ------------------#
        # la columna 'hora' la convertimos en formato datetime
        df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.time

        # Convertir las horas a minutos desde la medianoche

        df['minutos desde medianoche'] = df['Hora'].apply(lambda x: x.hour * 60 + x.minute)

        # Definir los límites de los intervalos de una hora
        intervalos = np.arange(0, 1441, 60)  # 1 hora = 60 minutos, desde las 00:00 hasta las 24:00

        # Aplicar pd.cut para agrupar los minutos en intervalos de una hora
        df['Intervalo hora'] = pd.cut(df['minutos desde medianoche'], bins=intervalos, labels=[f'{i}:00-{i+1}:00' for i in range(24)], right=False)


        # Definir las condiciones
        condiciones = [
            (df['Positivo alcohol'] == 1) & (df['Positivo droga'] == 0),
            (df['Positivo alcohol'] == 0) & (df['Positivo droga'] == 1),
            (df['Positivo alcohol'] == 1) & (df['Positivo droga'] == 1)
        ]

        # Definir los resultados correspondientes a las condiciones
        resultados = [
            'Positivo en Alcohol',
            'Positivo en Droga',
            'Positivo en Alcohol y Droga'
        ]
        # Crear nueva columna 'Positivos'
        df['Positivos'] = np.select(condiciones, resultados, default='Negativo')

        # Agrupar y sumar los datos por intervalo de horas, día de la semana y etiqueta de positivo
        df_positivos = df[df['Positivos'] != 'Negativo'].groupby(['Día semana', 'Intervalo hora', 'Positivos'],observed=False).size().reset_index(name='cantidad')

        # Convertir la columna 'Día semana' a un tipo de dato categórico con el orden deseado
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        # Definir un orden personalizado para los intervalos de Hora
        orden_horas = [f'{i}:00-{i+1}:00' for i in range(7, 24)] + [f'{i}:00-{i+1}:00' for i in range(0, 7)]
        
        # Crear el heatmap con Plotly
        heatmap_fig = px.density_heatmap(
            df_positivos,
            x='Intervalo hora',
            y='Día semana',
            z='cantidad',
            facet_col='Positivos',
            color_continuous_scale='Viridis',
            title='Implicados positivos en Alcohol/Drogas', 
            category_orders={'Intervalo hora': orden_horas, "Día semana": dias_semana}
        )

        heatmap_fig.update_layout(
            xaxis_title='Intervalo de Hora',
            yaxis_title='Día de la Semana',
            coloraxis_colorbar=dict(title='Implicados'),
            font=dict(family='Arial', size=12, color='white'),
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
            plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo transparente
        )

        heatmap_fig.update_xaxes(showgrid=False, zeroline=False, color='white')
        heatmap_fig.update_yaxes(showgrid=False, zeroline=False, color='white')


        st.plotly_chart(heatmap_fig, use_container_width=True)

        #? ---------------- Scatter Plot : Implicados positivos en Alcohol y Drogas  ------------------#
        # Mapear los valores de positivo a colores discretos
        color_map = { 
            'Positivo en Alcohol': 'lightblue', 
            'Positivo en Droga': 'yellow', 
            'Positivo en Alcohol y Droga': 'red'
        }

        # Crear el gráfico de dispersión con color y tamaño
        scatter_fig = px.scatter(
            df_positivos,
            x='Intervalo hora',
            y='Día semana',
            color='Positivos',
            color_discrete_map=color_map,  # Mapear los valores de positivo a colores discretos
            size='cantidad',  # Ajustar el tamaño de las burbujas si lo prefieres
            #hover_name='Tipo accidente',
            labels={'Intervalo hora': 'Intervalo de Hora del Accidente', 'Día semana': 'Día de la Semana', 'etiqueta_positivo': 'Resultado Pruebas Alcohol/Drogas'},
            title='Relación entre Intervalo de Hora y Día del Accidente, Pruebas Positivas de Alcohol/Drogas',
            category_orders={'Intervalo hora': orden_horas, "Día semana": dias_semana}  # Ordenar las horas
        )

        # Ajustar el diseño de la gráfica
        scatter_fig.update_layout(
            xaxis_title='Intervalo de Hora del Accidente',
            yaxis_title='Día del Accidente',  
            font=dict(family='Arial', size=12, color='black'),  # Personalizar la fuente
            legend=dict(title_font=dict(size=12), font=dict(size=10)),  # Personalizar la leyenda
            margin=dict(l=50, r=50, t=80, b=50),
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Fondo transparente
            plot_bgcolor='rgba(0, 0, 0, 0)'    # Fondo transparente# Ajustar los márgenes
            #hovermode='x'  # Activar el modo hover
        )

        scatter_fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
        
        # Mostrar la figura en Streamlit
        st.plotly_chart(scatter_fig, use_container_width=True)
        


        #? ---------------- Scatter Plot : Implicados positivos en Alcohol y Drogas  ------------------#

        # Contar los registros por cada valor en las columnas 'Positivos' y 'Lesividad'
        conteo_positivos_lesividad = df.groupby(['Positivos', 'Lesividad']).size().reset_index(name='Cantidad')


        # Crear la figura con subplots
        fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

        # Definir los colores
        colors = px.colors.sequential.Viridis #px.colors.sequential.Blues_r

        # Función para añadir trazas de Pie Chart
        def add_pie_trace(fig, data, row, col, name):
            fig.add_trace(
                go.Pie(
                    labels=data['Lesividad'],
                    values=data['Cantidad'],
                    name=name,textinfo='label+percent+value',showlegend=False,hole=.3,
                    marker=dict(colors=colors)
                ),
                row, col
            )

        # Añadir trazas de Pie Chart
        for i, positivo in enumerate(resultados):
            data = conteo_positivos_lesividad[conteo_positivos_lesividad['Positivos'] == positivo]
            add_pie_trace(fig, data, 1, i + 1, positivo)

        # Actualizar el diseño del gráfico
        fig.update_layout(
            title_text='Lesividad por positivo Alcohol/Drogas',
            annotations=[
                dict(text='   + Alcohol', x=0.1, y=0.5, font_size=16, showarrow=False),
                dict(text='+ Droga', x=0.5, y=0.5, font_size=16, showarrow=False),
                dict(text='+ Ambos     ', x=0.9, y=0.5, font_size=16, showarrow=False)
            ],
            showlegend=True
        )

        # Mostrar la figura en Streamlit
        st.plotly_chart(fig, use_container_width=True)





