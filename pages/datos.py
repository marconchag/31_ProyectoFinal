import streamlit as st
import utils

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)


if 'df' in st.session_state and 'df_agrupado' in st.session_state:
    df = st.session_state.df.copy()
    df_agrupado = st.session_state.df_agrupado.copy()
    # --------------------SIDEBAR----------------------------#
    utils.menu() #   👈

    #--------------------  TITULO PAGINA DE DATOS  ----------------------------#
    st.title("Datos usados en el análisis")

    #--------------------------DFS---------------------------#
    #mostrar df sin agrupar
    st.subheader("Data frame Implicados")
    st.write(df)
    st.subheader("Data frame Accidentes")
    st.write(df_agrupado)