# -------------------IMPORTACIONES----------------------#
import streamlit as st
# Importamos componentes
import utils
import estilos
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px 

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

#------------------Cargar Datos----------------------#


if 'df' in st.session_state and 'df_agrupado' in st.session_state:
    df = st.session_state.df.copy()
    df_agrupado = st.session_state.df_agrupado.copy()

    #*--------------------  TITULO PAGINA DE IMPLICADOS  ----------------------------#
    st.title("Registro de Accidentes ")

    #* --------------------SIDEBAR ------------------#
    utils.menu() #   👈

    #* --------------------Filtros ------------------#
    df = utils.filtros(['Año','Día semana','Distrito','Tipo accidente','Tramo horario', 'Estado meteorológico'],df)


    #?--------------------  Tarjeta principal  ----------------------------#
    accidentes = df_agrupado.shape[0]
    estilos.tarjeta_horizontal(accidentes, 'Número de accidentes') #   👈

    #?--------------------  Gráfico Barras : Total Accidentes por Año  ----------------------------#
    # Convertir la columna 'Fecha' al formato de Fecha adecuado
    df_agrupado['Fecha'] = pd.to_datetime(df_agrupado['Fecha'])

    # Agrupar por año y contar las ocurrencias
    total_por_año = df_agrupado.groupby(df_agrupado['Fecha'].dt.year)['Expediente'].nunique().reset_index(name='total_accidentes')
    total_por_año['porcentaje'] = (total_por_año['total_accidentes'] / total_por_año['total_accidentes'].sum()) * 100
    
    # Graficar utilizando Plotly Express
    fig = px.bar(
        x=total_por_año['Fecha'],
        y=total_por_año['total_accidentes'],
        color = total_por_año['total_accidentes'],
        color_continuous_scale=px.colors.sequential.Viridis,
        #text=total_por_año['porcentaje'].round(2).astype(str) + '%' ,
        text=[f'<b>{accidentes:,}'.replace(',', '.') + f'<br> ({porcentaje:.2f}%)</b>' for accidentes, porcentaje in zip(total_por_año['total_accidentes'], total_por_año['porcentaje'])],
        #textposition='auto',  # Colocar automáticamente el texto
        title='Total de Accidentes por Año'
    )
    # Actualizar el diseño del gráfico
    fig.update_layout(
        title_text="Total de Accidentes por Año",
        xaxis_title="Año",
        yaxis_title="Total de Accidentes"
    )
    # Desactivar la barra de colores continua
    fig.update_coloraxes(showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    #? -------------------- Mostramos las pestañas ----------------------------#
    # Pestañas para diferentes gráficos
    st.markdown("##### Más información")
    tpAccidente, tpVehiculo, lesividad, horarios, clima = st.tabs([ 
                                        "Tipo de accidente", "Tipo de vehículo", 
                                        "Lesividad","Tramo Horario/Día", 
                                        "Clima"])
    # CSS en las pestañas
    estilos.pestañas()


    with tpAccidente:
        #?-----Gráfico barras horizontales : Distribución de tipo de accidente----#
        # Contar el número de accidentes por tipo de accidente
        tipo_accidente_counts = df_agrupado['Tipo accidente'].value_counts()
        # Calcular el porcentaje de cada tipo de accidente
        total_accidentes = tipo_accidente_counts.sum()
        tipo_accidente_porcentaje = (tipo_accidente_counts / total_accidentes) * 100


        # Crear el gráfico de barras horizontales
        fig = px.bar(x=tipo_accidente_counts.values, 
                y=tipo_accidente_counts.index, 
                orientation='h', 
                text=[f'<b>{accidentes:,}'.replace(',', '.') + f'<br> ({porcentaje:.2f}%)</b>' for accidentes, porcentaje in zip(tipo_accidente_counts.values, tipo_accidente_porcentaje)],
                title='Distribución de Tipos de Accidente',
                labels={'index': 'Tipo de Accidente', 'Tipo accidente': 'Número de Accidentes'},
                color=tipo_accidente_counts.values,
                color_continuous_scale=px.colors.sequential.Viridis)

        # Actualizar el diseño del gráfico
        fig.update_layout(xaxis_title='Número de Accidentes',
                    yaxis_title='Tipo de Accidente',
                    yaxis={'categoryorder': 'total ascending'})
        # Desactivar la barra de colores continua
        fig.update_coloraxes(showscale=False)

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)
    with tpVehiculo:
        #?-----Gráfico barras horizontales : Distribución de tipo de accidente----#
# Contar el número de accidentes únicos por tipo de vehículo y ordenar de mayor a menor
        tpVehiculo_counts = df.groupby('Tipo vehiculo')['Expediente'].nunique().reset_index()
        tpVehiculo_counts = tpVehiculo_counts.sort_values(by='Expediente', ascending=True)

        # Calcular el porcentaje de cada tipo de vehículo
        total_accidentes = tpVehiculo_counts['Expediente'].sum()
        tpVehiculo_counts['porcentaje'] = (tpVehiculo_counts['Expediente'] / total_accidentes) * 100


        # Crear el gráfico de barras horizontal usando plotly.express
        fig = px.bar(tpVehiculo_counts,
                    x='Expediente',
                    y='Tipo vehiculo',
                    orientation='h',
                    # text = [f'{accidentes:,}'.replace(',', '.') + f'<br> ({porcentaje:.2f}%)'for accidentes, porcentaje in zip(tpVehiculo_counts['Expediente'], tpVehiculo_counts['porcentaje'])],
                    text=[f'<b>{accidentes:,}'.replace(',', '.') + f' ({porcentaje:.2f}%)</b>' for accidentes, porcentaje in zip(tpVehiculo_counts['Expediente'], tpVehiculo_counts['porcentaje'])],
                    color='Expediente',
                    color_continuous_scale=px.colors.sequential.Viridis,
                    title='Número de accidentes por tipo de vehículo')

        # Actualizar el diseño del gráfico
        fig.update_layout(
            xaxis_title='Número de accidentes',
            yaxis_title='Tipo de vehículo',
            template='plotly_dark',  # Mantener la plantilla oscura para una mejor visibilidad
            font=dict(family='Arial', size=12, color='white'),  # Personalizar la fuente
            margin=dict(l=100, r=50, t=80, b=50)  # Ajustar los márgenes
        )
        # Desactivar la barra de colores continua
        fig.update_coloraxes(showscale=False)
        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)


    #?-------Heatmap: relacion entre el tipo de accidente y el vehículo------# 

        # Crear una tabla de frecuencia cruzada (crosstab), para contar la frecuencia de cada combinación.
        crosstab = pd.crosstab(df_agrupado['Tipo accidente'], df['Tipo vehiculo'])

        # Convertir la tabla crosstab en un DataFrame para usar con plotly
        crosstab_reset = crosstab.reset_index()

        # Usar plotly.express para crear el heatmap interactivo
        fig = px.imshow(crosstab.values, 
                    labels=dict(x="Tipo de Vehículo", y="Tipo de Accidente", color="Frecuencia"),
                    x=crosstab.columns, 
                    y=crosstab.index,
                    color_continuous_scale=px.colors.sequential.Viridis,
                    aspect="auto",
                    text_auto=True)  # Esta línea agrega los números en las casillas

        # Personalizar el título y las etiquetas
        fig.update_layout(
            title='Relación entre Tipo de Accidente y Tipo de Vehículo',
            xaxis_title='Tipo de Vehículo',
            yaxis_title='Tipo de Accidente'
        )

        st.plotly_chart(fig, use_container_width=True)
    with lesividad:
    #? ----------Gráfico Barras: Accidente y tipo lesividad por tramo horario ----------#
    # Agrupar por día de la semana, tramo horario y tipo de lesividad y contar las ocurrencias
        total_por_dia_horario_lesividad = df.groupby(['Día semana', 'Tramo horario', 'Lesividad'])['Expediente'].nunique().reset_index(name='cantidad')
        total_por_dia_horario_lesividad.rename(columns={'Lesividad': 'Tipo Lesividad','Tramo horario':'Horario','Día semana':'Día'}, inplace=True)

        #* Convertir la columna 'Día' a tipo categórico con el orden específico
        dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        # Crear un gráfico por cada tramo horario
        for horario in total_por_dia_horario_lesividad['Horario'].unique():
            # Filtrar los datos por tramo horario
            datos_horario = total_por_dia_horario_lesividad[total_por_dia_horario_lesividad['Horario'] == horario]
        
            # Crear gráfico de barras
            fig = px.bar(datos_horario, x='Día', y='cantidad', color='Tipo Lesividad',
                    title=f'Accidentes y tipo de lesividad por día de la semana en el tramo horario {horario}',
                    labels={'Día semana': 'Día de la semana', 'cantidad': 'Cantidad de Accidentes'},
                    category_orders={'Día': dias_semana},
                    color_discrete_sequence=px.colors.sequential.Viridis)
        
            # Ajustar diseño
            fig.update_layout(xaxis_title='Día de la semana', yaxis_title='Cantidad de Accidentes')
        
            # Mostrar el gráfico
            st.plotly_chart(fig, use_container_width=True)


            


    with horarios:
        #? ----------Distribucón Accidentes por Horario y Sexo----------# 
        #accidentes por tramo horario y sexo!!!!!!!!!!!!!!!!!!!!!
        total_por_sexo = df.groupby(['Sexo']).size().reset_index(name='cantidad')
        total_por_horario = df_agrupado.groupby(['Tramo horario'])['Expediente'].nunique().reset_index(name='cantidad')

        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=total_por_horario['Tramo horario'].values,
                            values=total_por_horario['cantidad'].values,
                            name='',textinfo='label+percent',showlegend=False,hole=.3, 
                            marker_colors=px.colors.sequential.Viridis),1,1)

        fig.add_trace(go.Pie(labels=total_por_sexo['Sexo'].values,
                            values=total_por_sexo['cantidad'].values,
                            name='',textinfo='label+percent',showlegend=False,hole=.3, 
                            marker_colors=px.colors.sequential.Viridis),1,2)

        # Actualizar el diseño del gráfico
        fig.update_layout(title_text="Distribución Accidentes por Horario y Sexo")

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)


    #?--------------- Gráfico de Barras : Accidentes por Franja horaria y tipo de Implicado -----------------#
        #nº de acccidentes segun granja horaria: 
        # Definir el orden de los tramos horarios
        orden_tramos = ['Mañana', 'Tarde', 'Noche', 'Madrugada']

        # Convertir la columna 'Tramo horario' a tipo categórico con el orden específico
        df['Tramo horario'] = pd.Categorical(df['Tramo horario'], categories=orden_tramos, ordered=True)

        # Ordenar el DataFrame según el orden de los tramos horarios
        df_sorted = df.sort_values(by='Tramo horario')

        # Crear el histograma con Plotly Express
        fig = px.histogram(df_sorted, 
                        x='Tramo horario', 
                        color='Implicado', 
                        barmode='group', 
                        title='Accidentes por Franja Horaria y Tipo de Implicado', 
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        labels={'Tramo horario': 'Franja Horaria', 'count': 'Número de Accidentes', 'Implicado': 'Tipo de Persona'})

        # Actualizar el diseño del gráfico
        fig.update_layout(
            xaxis_title='Franja Horaria',
            yaxis_title='Número de Accidentes',
            legend_title='Tipo de Persona'
        )

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)



    #?-----Gráfico barras: Accidentes en días laborables vs Festivos ----#
        fig = px.histogram(df_agrupado, 
                    x='Tipo día', 
                    color='Día semana', 
                    barmode='group', 
                    title='Accidentes en Días Laborables vs. Festivos', 
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    labels={'Tipo día':'Día de la Semana', 'count':'Número de Accidentes', 'Día semana':'Día de la Semana'})

        fig.update_layout(
            xaxis_title='Día de la Semana',
            yaxis_title='Número de Accidentes',
            legend_title='Día de la Semana'
            )

        #Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)
    with clima:
    #?-----------------Gráfico de Barras : Relacción entre Tipo de Accidentes y Estado Meteorológico-----------------#
        # Crear una tabla de frecuencia cruzada (crosstab)
        crosstab2 = pd.crosstab(df_agrupado['Tipo accidente'], df_agrupado['Estado meteorológico'])

        # Crear un DataFrame a partir del crosstab
        crosstab_df = crosstab2.reset_index().melt(id_vars='Tipo accidente', value_name='Frecuencia')

        # Crear un gráfico de barras agrupadas usando Plotly Express
        fig = px.bar(crosstab_df, 
                    x='Tipo accidente', 
                    y='Frecuencia', 
                    color='Estado meteorológico', 
                    title='Relación entre Tipo de Accidente y Estado Meteorológico', 
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    labels={'Tipo accidente':'Tipo de Accidente', 'Frecuencia':'Frecuencia', 'Estado meteorológico':'Estado Meteorológico'})

        # Personalizar el gráfico
        fig.update_layout(
            xaxis_title='Tipo de Accidente',
            yaxis_title='Frecuencia',
            legend_title='Estado Meteorológico',
            legend_font_size=12,
            legend_title_font_size=14)

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)