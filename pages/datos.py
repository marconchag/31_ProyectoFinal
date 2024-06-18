import streamlit as st
import base64
import utils

# Función para descargar el DataFrame como CSV
@st.cache_data(show_spinner=False)
def descargar_csv(dataframe):
    csv = dataframe.to_csv(index=False).encode('utf-8')
    b64 = base64.b64encode(csv).decode()  # Codificar en base64
    return b64

# Asignamos la configuración de la página
st.set_page_config(**utils.confPage)

# Verificar si los datos están en la sesión
if 'df' in st.session_state and 'df_agrupado' in st.session_state:
    # SIDEBAR
    utils.menu()

    # Mostrar el botón de descarga para el DataFrame de Implicados
    st.subheader("Data frame Implicados")
    if st.button('Descargar Datos Implicados'):
        with st.spinner('Generando archivo...'):
            b64 = descargar_csv(st.session_state.df)
            
        # Crear enlace de descarga
        href = f'data:text/csv;base64,{b64}'
        # Mostrar enlace de descarga guardado
        st.markdown(f'<a href="{href}" download="implicados.csv" class="download-link">'
                    '<i class="fas fa-download"></i> Descargar CSV Implicados</a>',
                    unsafe_allow_html=True)
    
    st.write(st.session_state.df)

    # Mostrar el botón de descarga para el DataFrame de Accidentes
    st.subheader("Data frame Accidentes")
    if st.button('Descargar Datos Accidentes'):
        with st.spinner('Generando archivo...'):
            b64 = descargar_csv(st.session_state.df_agrupado)
            
        # Crear enlace de descarga
        href = f'data:text/csv;base64,{b64}'
        # Mostrar enlace de descarga guardado
        st.markdown(f'<a href="{href}" download="accidentes.csv" class="download-link">'
                    '<i class="fas fa-download"></i> Descargar CSV Accidentes</a>',
                    unsafe_allow_html=True)
    
    st.write(st.session_state.df_agrupado)
