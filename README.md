# Proyecto Final - Análisis de Accidentes de Tráfico en Madrid

![Banner](./img/ComMadrid.png)

---

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

- **Aplicación**
  - `app.py`: Aplicación Streamlit para interactuar con los datos y modelos.
  - `estilos.py`: Estilos personalizados para la aplicación.
  - `utils.py`: Funciones utilitarias.

## Fuente de datos
  - `app.py`: Aplicación Streamlit para interactuar con los datos y modelos.

## Requisitos

Instala las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt


