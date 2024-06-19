import streamlit as st
import pandas as pd
import base64

#* --------------------Asignamos la configuracion de la página para utilizarlo ponemos ------------------ 
#* st.set_page_config(**confPage) ** Sirven para desempaquetar un diccionario como clave y valor ------------------#

confPage = {
    'page_title': 'Accidentes de tráfico de la Comunidad de Madrid',
    'page_icon': ':car:',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}
def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    st.sidebar.image(r'img/ComMadrid.png',use_column_width=True)
    st.sidebar.page_link("pages/datos.py", label="Datos")
    st.sidebar.page_link("app.py", label="Resumen")
    st.sidebar.page_link("pages/accidentes.py", label="Accidentes")
    st.sidebar.page_link("pages/implicados.py", label="Implicados")

    #Dejamos comentado el enlace a la página de predicciones hasta que tengamos los puntos de Azure
    #st.sidebar.page_link("pages/predicciones.py", label="Predicción")
    st.sidebar.markdown("""
    ---
    """)

def filtros(filtros, df, df_agrupado=None):
    #--------------------  BARRA LATERAL  ----------------------------#
    # Crear la barra lateral con filtros
    for columna in filtros:
        if columna == 'Año':
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            años = sorted(df['Fecha'].dt.year.unique())
            años_seleccionados = st.sidebar.slider(
                "Selecciona un rango de años",
                min_value=min(años),
                max_value=max(años),
                value=(min(años), max(años)),
                step=1
            )
            df = df[(df['Fecha'].dt.year >= años_seleccionados[0]) & (df['Fecha'].dt.year <= años_seleccionados[1])]
            if df_agrupado is not None:
                df_agrupado['Fecha'] = pd.to_datetime(df_agrupado['Fecha'])
                df_agrupado = df_agrupado[(df_agrupado['Fecha'].dt.year >= años_seleccionados[0]) & (df_agrupado['Fecha'].dt.year <= años_seleccionados[1])]
        else:
            opciones = df[columna].unique()
            seleccion = st.sidebar.multiselect(f'{columna}', opciones, opciones)
            if seleccion:
                    df = df[df[columna].isin(seleccion)]
                    if df_agrupado is not None:
                        df_agrupado = df_agrupado[df_agrupado[columna].isin(seleccion)]
    if df_agrupado is not None:
        return df, df_agrupado
    else:   
        return df 
