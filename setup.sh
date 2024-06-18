#!/bin/bash

# Instala las dependencias comunes
pip install pandas==2.1.4
pip install numpy==1.26.4
pip install streamlit==1.35.0
pip install plotly==5.22.0
pip install openpyxl==3.1.2
pip install scikit-learn==1.4.2
pip install xgboost==1.7.4
pip install matplotlib==3.7.5

# Instala pywin32 solo si el sistema operativo es Windows
if [[ "$OSTYPE" == "msys" ]]; then
    pip install pywin32==306
fi
