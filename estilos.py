import streamlit as st

color_grafico = 'Blues' # Color de los gráficos

def pestañas():
    
    #ESTILO DE LAS PESTAÑAS 
    return st.markdown("""
    <style>
        .stTabs [role="tablist"] {
            display: flex;
            flex-wrap: wrap;
            background-color: #1E1E1E ; 
            border-radius: 5px;ºº
            padding: 5px;
        }
        .stTabs [role="tab"] {
            flex: 1;
            text-align: center;
            color: white;
            font-weight: bold;
            margin: 2px;
            padding: 10px;
            border-radius: 5px;
            font-size: 30px; /* Tamaño de letra más grande */
        }
        .stTabs [role="tab"]:hover {
            background-color: #104E8B; /* Color más oscuro al pasar el mouse */
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #104E8B; /* Color de la pestaña seleccionada */
            border-bottom: 2px solid white;
        }
        .stTabs .css-1hynvyr, .stTabs .css-1o3i7jx, .stTabs .css-k1ih3n {
            background-color: #1E90FF; /* Fondo azul para el contenido */
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    
def tarjeta_horizontal(valor, titulo):
    valor_formateado = '{:,}'.format(valor).replace(',', '.')
    st.markdown(f"""
        <div class="metric-tarjeta">
            <div class="metric-titulo">{titulo}</div>
            <div class="metric-valor">{valor_formateado}</div>
        </div>
        <style>
        .metric-tarjeta {{
            background-color: #1E1E1E;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            color: white;
        }}
        .metric-titulo {{
            font-size: 24px;
            font-weight: bold;
            text-align: center;
        }}
        .metric-valor {{
            font-size: 40px; 
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    
def tarjeta(columna):
    tarjeta_html = """
    <div class="tarjetas-container">
    <div class="tarjetas-titulo">Por Lesividad</div>"""
    for titulo, valor in columna.items():
        valor_formateado = '{:,}'.format(valor).replace(',', '.')
        tarjeta_html += f"""
        <div class="tarjeta">
            <h4>{titulo}</h4>
            <p>{valor_formateado}</p>
        </div>"""
    tarjeta_html += """
    <style>
    .tarjeta {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        color: white;
        text-align: center;
        font-size: 12px;
    }
    .tarjetas-container {
        position: sticky;
        top: 50px;
        right: 30px;
        width: 200px;
        z-index: 1000;
    }
    .tarjetas-titulo {
        color: blue;
        text-align: center;
        margin-bottom: 10px;
        font-size: 28px;
    }
    .tarjeta p {
        font-size: 20px;
    }
    </style>
    </div>"""
    return tarjeta_html

def generar_tarjetas(datos):
    tarjeta_html = """
    <div class="container">"""
    for titulo, valor in datos.items():
        tarjeta_html += f"""
        <div class="col">
            <div class="card">
                <div class="title">{titulo}</div>
                <div class="data">{valor}</div>
            </div>
        </div>"""
        
    tarjeta_html += """
    </div>
    <style>
        .card {
            padding: 15px;
            margin: 10px;
            border-radius: 10px;
            background-color: #f8f9fa;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
            width: 100%;
        }
        .highlight {
            color: #ff4d4d;
            font-weight: bold;
        }
        .title {
            font-size: 20px;
            color: #333333;
        }
        .subtitle {
            font-size: 14px;
            color: #666666;
        }
        .data {
            font-size: 28px;
            color: #007bff;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin: 20px auto; /* Añadido para centrar el contenido */
            max-width: 1200px; /* Añadido para limitar el ancho máximo */
        }
        .col {
            flex: 0 0 calc(33.33% - 20px); /* Calculamos el 33.33% para 3 columnas y restamos el margen */
            max-width: calc(33.33% - 20px); /* Igual que arriba */
        }
        @media (max-width: 768px) {
            .col {
                flex: 0 0 100%;
                max-width: 100%;
            }
        }
    </style> """
    
    return tarjeta_html


