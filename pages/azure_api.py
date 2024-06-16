import streamlit as st
import urllib.request
import json 
import ssl 
import utils
from datetime import timedelta, date
from dotenv import load_dotenv
import os

#* --------------------Asignamos la configuracion de la página  ------------------#
st.set_page_config(**utils.confPage)


#* --------------------Cargamos las variables de entorno ------------------#
load_dotenv()
ssl._create_default_https_context = ssl._create_stdlib_context
URL = os.getenv('AZURE_ST_URL')
API = os.getenv('AZURE_ST_API')

#* --------------------SIDEBAR ------------------#
utils.menu()


st.title('Accidentes Madrid')

#creamos selectores para elegir barrio y tipo de habitación
Fecha = st.date_input("Seleccione una fecha:", min_value=date.today()+timedelta(days=1))


if st.button('Realizar prediccion'):
    data = {"input_data": {
"columns":["Fecha"],
"index":[0],
"data":[str(Fecha)]
}
}

    body = str.encode(json.dumps(data))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Bearer ' + API)
    }

    try:
        req = urllib.request.Request(URL, body, headers)

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf8", 'ignore'))
            st.write(int(result[0]))

    except urllib.error.HTTPError as error:
        print('The request failed with status code: ', str(error.code))
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))