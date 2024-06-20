# Proyecto Final - Análisis de Accidentes de Tráfico en Madrid

![Banner](./img/ComMadrid.png)
## Integrantes:
- Irene Bañon
- Lya Fiol
- Mar García

## Descripción

Este proyecto tiene como objetivo analizar los accidentes de tráfico en Madrid utilizando diversas herramientas de ciencia de datos y aprendizaje automático. A través de la limpieza y procesamiento de datos, visualización y modelado predictivo, buscamos entender patrones y factores que influyen en la siniestralidad vial.

## Estructura del Proyecto

- **Datos**
  - `datos`: Datos crudos de los accidentes.
  - `datos_procesados`: Datos después de la limpieza y transformación.

- **Modelos**
  - `modelos`: Contiene los modelos entrenados y sus evaluaciones.

- **Notebooks**
  - `00_ProcesamientoDatos.ipynb`: Limpieza y procesamiento de datos.
  - `01_Graficos.ipynb`: Visualizaciones exploratorias.
  - `02_pycaret_Accidentes.ipynb`: Modelado predictivo para accidentes.
  - `02_pycaret_Lesividad.ipynb`: Modelado predictivo para la lesividad.
    
- **Paginas**
  - `pages`: Contiene las páginas en nuestra aplicación Streamlit.
    
 - **Imágenes**
  - `img`: Contiene las imágenes utilizadas.
    
- **Aplicación**
  - `app.py`: Aplicación Streamlit para interactuar con los datos y modelos.
  - `estilos.py`: Estilos personalizados para la aplicación.
  - `utils.py`: Funciones utilitarias.
  - `app.py`: Aplicación Streamlit para interactuar con los datos y modelos.
  
    
## Fuente de datos
  -  https://accidentesmadrid.streamlit.app/ Nuestra app de Streamlit.
  -  Los datos de los distritos provienen del "Portal web del Ayuntamiento de Madrid" . "https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=33cb30c367e78410VgnVCM1000000b205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default"
  -  Los datos acerca de la latitud y longitud provienen de "Geodata"
  -  Para Streamlit https://docs.streamlit.io/
  -  https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=b3c41f3cf6a6c410VgnVCM2000000c205a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD
  

## Requisitos

Instala las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt


