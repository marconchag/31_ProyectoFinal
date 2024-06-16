import streamlit as st
import utils

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)

#------------------Cargar Datos----------------------#
# Definir una función para cargar los datos

# Definir una función para cargar los datos


if 'df' in st.session_state and 'df_agrupado' in st.session_state:

    df = st.session_state.df.copy()


    df_agrupado = st.session_state.df_agrupado.copy()


    # --------------------SIDEBAR----------------------------#
    utils.menu() #   👈

    #--------------------  TITULO PAGINA DE DATOS  ----------------------------#
    st.title("Datos usados en el análisis")

    #--------------------  BARRA LATERAL  ----------------------------#
    df = utils.filtros(['Año','Día semana','Distrito','Tipo accidente','Tramo horario', 'Estado meteorológico'],df)
    # df_agrupado = utils.filtros(['Año','Día semana','Distrito','Tipo accidente','Tramo horario', 'Estado meteorológico'],df_agrupado)

    #--------------------------DFS---------------------------#
    #mostrar df sin agrupar
    st.subheader("Data frame original")
    st.write(df)
    st.subheader("Data frame agrupado")
    st.write(df_agrupado)