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
    st.sidebar.page_link("app.py", label="Resumen")
    st.sidebar.page_link("pages/accidentes.py", label="Accidentes")
    st.sidebar.page_link("pages/implicados.py", label="Implicados")
    st.sidebar.page_link("pages/datos.py", label="Datos")
    st.sidebar.page_link("pages/azure_api.py", label="Predicción Azure")
    st.sidebar.page_link("pages/lesividad_azure.py", label="Lesividad Azure")
    st.sidebar.page_link("pages/predicciones.py", label="Predicción Pycaret")
    st.sidebar.markdown("""
    ---
    """)

def filtros(filtros, df):
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
        else:
            opciones = df[columna].unique()
            seleccion = st.sidebar.multiselect(f'{columna}', opciones, opciones)
            if seleccion:
                df = df[df[columna].isin(seleccion)]
    return df
