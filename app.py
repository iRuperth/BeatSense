# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# import plotly.express as px
# from datetime import datetime
# import joblib
# import os
# from sklearn.preprocessing import StandardScaler
# import json
# from streamlit_lottie import st_lottie

# HISTORY_FILE = "./assest/Heart with ECG.json"

# def load_history():
#     if os.path.exists(HISTORY_FILE):
#         with open(HISTORY_FILE, "r") as f:
#             data = json.load(f)
#             return data if isinstance(data, list) else []
#     return []

# st.set_page_config(
#     page_title="CardioPredict Pro | Sistema de Predicción Cardíaca",
#     page_icon="❤️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
#  # ESTILOS PERSONALIZADOS
# st.markdown("""
# <style>
#     /* Importar fuente profesional */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
#     /* Variables de color */
#     :root {
#         --primary-red: #E63946;
#         --dark-bg: #1A1A1A;
#         --light-bg: #F5F5F5;
#         --text-dark: #2C2C2C;
#         --text-light: #666666;
#     }
    
#     /* Estilos generales */
#     .main {
#         background-color: #F5F5F5;
#         font-family: 'Inter', sans-serif;
#     }
    
#     /* Header principal */
#     .main-header {
#         background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%);
#         padding: 2rem;
#         border-radius: 15px;
#         margin-bottom: 2rem;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#     }
    
#     .main-header h1 {
#         color: white;
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin: 0;
#         display: flex;
#         align-items: center;
#         gap: 1rem;
#     }
    
#     .main-header p {
#         color: #CCCCCC;
#         font-size: 1.1rem;
#         margin-top: 0.5rem;
#     }
    
#     /* Cards de métricas */
#     .metric-card {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 12px;
#         box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
#         border-left: 4px solid #E63946;
#         margin-bottom: 1rem;
#     }
    
#     .metric-card h3 {
#         color: #1A1A1A;
#         font-size: 0.9rem;
#         font-weight: 600;
#         margin: 0 0 0.5rem 0;
#         text-transform: uppercase;
#         letter-spacing: 0.5px;
#     }
    
#     .metric-card .value {
#         color: #E63946;
#         font-size: 2rem;
#         font-weight: 700;
#     }
    
#     .metric-card .value-text {
#         color: #E63946;
#         font-size: 1.3rem;
#         font-weight: 700;
#     }
    
#     /* Panel de resultados */
#     .result-panel {
#         background: white;
#         padding: 2rem;
#         border-radius: 15px;
#         box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
#         margin: 1rem 0;
#     }
    
#     .risk-high {
#         background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
#         color: white;
#         padding: 2rem;
#         border-radius: 15px;
#         text-align: center;
#     }
    
#     .risk-low {
#         background: linear-gradient(135deg, #06D6A0 0%, #05B389 100%);
#         color: white;
#         padding: 2rem;
#         border-radius: 15px;
#         text-align: center;
#     }
    
#     .risk-high h2, .risk-low h2 {
#         font-size: 2rem;
#         margin: 0;
#         font-weight: 700;
#     }
    
#     .risk-high p, .risk-low p {
#         font-size: 1.1rem;
#         margin: 0.5rem 0 0 0;
#         opacity: 0.9;
#     }
    
#     /* Botón principal */
#     .stButton > button {
#         background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
#         color: white;
#         border: none;
#         padding: 0.75rem 2rem;
#         font-size: 1.1rem;
#         font-weight: 600;
#         border-radius: 8px;
#         width: 100%;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 6px rgba(230, 57, 70, 0.3);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 8px rgba(230, 57, 70, 0.4);
#     }
    
#     /* Info boxes */
#     .info-box {
#         background: #FFF4E6;
#         border-left: 4px solid #FF9500;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     .warning-box {
#         background: #FFE5E5;
#         border-left: 4px solid #E63946;
#         padding: 1rem;
#         border-radius: 8px;
#         margin: 1rem 0;
#     }
    
#     /* Footer */
#     .footer {
#         text-align: center;
#         padding: 2rem;
#         color: #666666;
#         font-size: 0.9rem;
#         margin-top: 3rem;
#     }
# </style>
# """, unsafe_allow_html=True)

# # FUNCION PARA CARGAR MI GIT
# def load_lottiefile(filepath: str):
#     """Carga una animación Lottie desde un archivo JSON local."""
#     if os.path.exists(filepath):
#         with open(filepath, "r") as f:
#             return json.load(f)
#     return None

# @st.cache_resource
# def cargar_modelo():
#     """
#     Carga el modelo entrenado y el scaler.
#     Busca en la carpeta 'models' los archivos .pkl
#     """
#     try:
#         # Intentar cargar desde la carpeta models
#         modelo = joblib.load('models/modelo_coronario.pkl')
#         scaler = joblib.load('models/scaler_coronario.pkl')
#         return modelo, scaler, True
#     except FileNotFoundError:
#         st.error(" No se encontraron los archivos del modelo. Asegúrate de tener la carpeta 'models' con los archivos 'modelo_coronario.pkl' y 'scaler_coronario.pkl'")
#         return None, None, False
# def preparar_datos_para_prediccion(datos, scaler):
#     """
#     Prepara los datos del paciente en el formato correcto para el modelo.
#     Aplica one-hot encoding y escalado según fue entrenado el modelo.
#     """
#     # Crear las columnas one-hot para ChestPainType
#     cp_asy = 1 if datos['chest_pain_type'] == 'ASY' else 0
#     cp_ata = 1 if datos['chest_pain_type'] == 'ATA' else 0
#     cp_nap = 1 if datos['chest_pain_type'] == 'NAP' else 0
#     cp_ta = 1 if datos['chest_pain_type'] == 'TA' else 0
    
#     # Crear las columnas one-hot para ST_Slope
#     st_slope_flat = 1 if datos['st_slope'] == 'Flat' else 0
#     st_slope_up = 1 if datos['st_slope'] == 'Up' else 0
#     st_slope_down = 1 if datos['st_slope'] == 'Down' else 0
    
#     # ExerciseAngina convertido a binario
#     exercise_angina_bin = 1 if datos['exercise_angina'] == "Sí" else 0
    
#     # Crear DataFrame con todas las features en el orden correcto
#     X = pd.DataFrame([[
#         datos['age'],              # Age (se escalará)
#         datos['sex'],              # Sex
#         datos['max_hr'],           # MaxHR (se escalará)
#         datos['fasting_bs'],       # FastingBS
#         exercise_angina_bin,       # ExerciseAngina
#         cp_asy,                    # CP_ASY
#         cp_ata,                    # CP_ATA
#         cp_nap,                    # CP_NAP
#         cp_ta,                     # CP_TA
#         st_slope_flat,             # ST_Slope_Flat
#         st_slope_up,               # ST_Slope_Up
#         st_slope_down              # ST_Slope_Down
#     ]], columns=[
#         'Age', 'Sex', 'MaxHR', 'FastingBS', 'ExerciseAngina',
#         'CP_ASY', 'CP_ATA', 'CP_NAP', 'CP_TA',
#         'ST_Slope_Flat', 'ST_Slope_Up', 'ST_Slope_Down'
#     ])
    
#     # Aplicar escalado SOLO a Age y MaxHR (igual que en el entrenamiento)
#     X_scaled = X.copy()
#     cols_para_escalar = ['Age', 'MaxHR']
#     X_scaled[cols_para_escalar] = scaler.transform(X[cols_para_escalar])
    
#     return X_scaled

# def predecir_riesgo(datos, modelo, scaler):
#     """
#     Realiza la predicción de riesgo cardíaco usando el modelo real.
#     """
#     if modelo is None or scaler is None:
#         return 0, "Sin modelo", [0, 0]
    
#     # Preparar los datos
#     X_preparado = preparar_datos_para_prediccion(datos, scaler)
    
#     # Realizar predicción
#     probabilidades = modelo.predict_proba(X_preparado)[0]
#     probabilidad_enfermedad = probabilidades[1] * 100  # Probabilidad de clase 1 (enfermo)
    
#     # Clasificación (usando umbral de 40% como en el entrenamiento)
#     clasificacion = "Alto Riesgo" if probabilidad_enfermedad >= 40 else "Bajo Riesgo"
    
#     return probabilidad_enfermedad, clasificacion, probabilidades

# def crear_gauge_chart(probabilidad):
#     """Crea un medidor visual del riesgo"""
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number+delta",
#         value=probabilidad,
#         domain={'x': [0, 1], 'y': [0, 1]},
#         title={'text': "Nivel de Riesgo (%)", 'font': {'size': 24, 'color': '#1A1A1A'}},
#         delta={'reference': 40, 'increasing': {'color': "#E63946"}, 'decreasing': {'color': "#06D6A0"}},
#         gauge={
#             'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#1A1A1A"},
#             'bar': {'color': "#E63946" if probabilidad >= 40 else "#06D6A0"},
#             'bgcolor': "white",
#             'borderwidth': 2,
#             'bordercolor': "#E0E0E0",
#             'steps': [
#                 {'range': [0, 40], 'color': '#E8F5E9'},
#                 {'range': [40, 70], 'color': '#FFF4E6'},
#                 {'range': [70, 100], 'color': '#FFE5E5'}
#             ],
#             'threshold': {
#                 'line': {'color': "#E63946", 'width': 4},
#                 'thickness': 0.75,
#                 'value': 90
#             }
#         }
#     ))
    
#     fig.update_layout(
#         paper_bgcolor="white",
#         font={'color': "#1A1A1A", 'family': "Inter"},
#         height=350
#     )
    
#     return fig

# def crear_radar_chart(datos):
#     """Crea un gráfico de radar con los factores de riesgo"""
#     categorias = ['Edad', 'Frec. Cardíaca', 'Glucosa', 'Tipo Dolor', 'Angina', 'Pendiente ST']
    
#     # Normalizar valores a escala 0-100
#     valores = [
#         min((datos['age'] / 100) * 100, 100),
#         min((datos['max_hr'] / 200) * 100, 100),
#         datos['fasting_bs'] * 100,
#         {'ASY': 100, 'TA': 75, 'ATA': 50, 'NAP': 25}[datos['chest_pain_type']],
#         100 if datos['exercise_angina'] == "Sí" else 0,
#         {'Flat': 100, 'Down': 75, 'Up': 25}[datos['st_slope']]
#     ]
    
#     fig = go.Figure()
    
#     fig.add_trace(go.Scatterpolar(
#         r=valores,
#         theta=categorias,
#         fill='toself',
#         fillcolor='rgba(230, 57, 70, 0.3)',
#         line=dict(color='#E63946', width=2),
#         name='Factores del Paciente'
#     ))
    
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 100],
#                 gridcolor='#E0E0E0'
#             ),
#             bgcolor='white'
#         ),
#         showlegend=False,
#         paper_bgcolor='white',
#         font={'color': "#1A1A1A", 'family': "Inter"},
#         height=400
#     )
    
#     return fig

# # =====================================================================
# # CARGAR MODELO
# # =====================================================================
# modelo, scaler, modelo_cargado = cargar_modelo()

# # =====================================================================
# # HEADER DE LA APLICACIÓN
# # =====================================================================
# st.markdown("""
# <div class="main-header">
#     <h1>❤️ CardioPredict Pro</h1>
#     <p>Sistema Inteligente de Evaluación de Riesgo Cardiovascular | Regresión Logística Médica</p>
# </div>
# """, unsafe_allow_html=True)

# if not modelo_cargado:
#     st.warning("""
#     ### 📁 Instrucciones para cargar el modelo:
    
#     1. Crea una carpeta llamada `models` en el mismo directorio que esta aplicación
#     2. Coloca los siguientes archivos dentro de la carpeta `models`:
#        - `modelo_coronario.pkl` (tu modelo entrenado)
#        - `scaler_coronario.pkl` (tu scaler entrenado)
#     3. Recarga la aplicación
    
#     **Estructura esperada:**
#     ```
#     tu_proyecto/
#     ├── app.py (este archivo)
#     ├── models/
#     │   ├── modelo_coronario.pkl
#     │   └── scaler_coronario.pkl
#     └── .streamlit/
#         └── config.toml
#     ```
#     """)
#     st.stop()

# # =====================================================================
# # SIDEBAR - ENTRADA DE DATOS
# # =====================================================================
# with st.sidebar:
#     st.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
#     st.title("📋 Datos del Paciente")
#     st.markdown("---")
    
#     # Información del paciente
#     st.subheader("🆔 Información General")
    
#     patient_id = st.text_input("ID del Paciente", placeholder="Ej: PAC-2024-001")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         age = st.number_input("Edad", min_value=1, max_value=120, value=50, step=1)
#     with col2:
#         sex = st.selectbox("Sexo", ["Masculino", "Femenino"])
    
#     st.markdown("---")
#     st.subheader("🔬 Parámetros Cardíacos")
    
#     # Frecuencia cardíaca máxima
#     max_hr = st.number_input(
#         "Frecuencia Cardíaca Máxima (bpm)",
#         min_value=60,
#         max_value=220,
#         value=150,
#         step=1,
#         help="Frecuencia cardíaca máxima alcanzada durante ejercicio"
#     )
    
#     # Glucosa
#     fasting_bs = st.selectbox(
#         "Glucosa en Ayunas > 120 mg/dl",
#         [0, 1],
#         format_func=lambda x: "No" if x == 0 else "Sí",
#         help="Indica si la glucosa en ayunas supera los 120 mg/dl"
#     )
    
#     st.markdown("---")
#     st.subheader("💔 Síntomas y ECG")
    
#     # Angina inducida por ejercicio
#     exercise_angina = st.selectbox(
#         "Angina Inducida por Ejercicio",
#         ["No", "Sí"],
#         help="Dolor torácico durante actividad física"
#     )
    
#     # Tipo de dolor torácico (ChestPainType)
#     chest_pain_type = st.selectbox(
#         "Tipo de Dolor Torácico",
#         ["ASY", "ATA", "NAP", "TA"],
#         format_func=lambda x: {
#             "ASY": "Asintomático",
#             "ATA": "Angina Atípica",
#             "NAP": "Dolor No Anginoso",
#             "TA": "Angina Típica"
#         }[x],
#         help="Tipo de dolor en el pecho reportado por el paciente"
#     )
    
#     # Pendiente del segmento ST
#     st_slope = st.selectbox(
#         "Pendiente del Segmento ST",
#         ["Flat", "Up", "Down"],
#         format_func=lambda x: {
#             "Flat": "Plana",
#             "Up": "Ascendente",
#             "Down": "Descendente"
#         }[x],
#         help="Pendiente del segmento ST en el electrocardiograma de esfuerzo"
#     )
    
#     st.markdown("---")
    
#     # Botón de análisis
#     analizar = st.button("🔍 ANALIZAR RIESGO CARDÍACO", use_container_width=True)
    
#     # st.markdown("---")
#     # st.caption("⚕️ Desarrollado para profesionales médicos")
#     # st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
#     # st.caption("🤖 Modelo: Regresión Logística")

# # =====================================================================
# # CONTENIDO PRINCIPAL
# # =====================================================================

# # Crear tabs para organizar la información
# tab1, tab2, tab3 = st.tabs(["📊 Análisis de Riesgo", "📈 Visualizaciones", "ℹ️ Información Médica"])

# with tab1:
#     if analizar:
#         # Preparar datos
#         datos_paciente = {
#             'age': age,
#             'sex': 1 if sex == "Masculino" else 0,
#             'max_hr': max_hr,
#             'fasting_bs': fasting_bs,
#             'exercise_angina': exercise_angina,
#             'chest_pain_type': chest_pain_type,
#             'st_slope': st_slope
#         }
        
#         # Realizar predicción
#         probabilidad, clasificacion, probs = predecir_riesgo(datos_paciente, modelo, scaler)
        
#         # Mostrar resultado principal
#         if clasificacion == "Alto Riesgo":
#             st.markdown(f"""
#             <div class="risk-high">
#                 <h2>⚠️ ALTO RIESGO DETECTADO</h2>
#                 <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="risk-low">
#                 <h2>✓ RIESGO BAJO</h2>
#                 <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # Métricas en columnas
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>📅 Edad</h3>
#                 <div class="value">{age}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>❤️ FC Máxima</h3>
#                 <div class="value">{max_hr}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col3:
#             dolor_texto = {
#                 "ASY": "Asintomático",
#                 "ATA": "Ang. Atípica",
#                 "NAP": "No Anginoso",
#                 "TA": "Ang. Típica"
#             }[chest_pain_type]
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>💔 Tipo Dolor</h3>
#                 <div class="value-text">{dolor_texto}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         with col4:
#             slope_texto = {
#                 "Flat": "Plana",
#                 "Up": "Ascendente",
#                 "Down": "Descendente"
#             }[st_slope]
#             st.markdown(f"""
#             <div class="metric-card">
#                 <h3>📉 Pendiente ST</h3>
#                 <div class="value-text">{slope_texto}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Probabilidades detalladas
#         st.markdown("<br>", unsafe_allow_html=True)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Probabilidad Sin Enfermedad", f"{probs[0]*100:.1f}%", 
#                      delta=None, delta_color="normal")
#         with col2:
#             st.metric("Probabilidad Con Enfermedad", f"{probs[1]*100:.1f}%", 
#                      delta=None, delta_color="inverse")
        
#         # Recomendaciones
#         st.markdown("<br>", unsafe_allow_html=True)
#         st.subheader("📋 Recomendaciones Médicas")
        
#         if clasificacion == "Alto Riesgo":
#             st.markdown("""
#             <div class="warning-box">
#                 <strong>⚠️ Acciones Recomendadas:</strong>
#                 <ul>
#                     <li>Evaluación cardiológica completa de forma urgente</li>
#                     <li>Electrocardiograma de 12 derivaciones</li>
#                     <li>Ecocardiograma y prueba de esfuerzo supervisada</li>
#                     <li>Analítica completa incluyendo perfil lipídico</li>
#                     <li>Considerar derivación a unidad de cardiología</li>
#                 </ul>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="info-box">
#                 <strong>✓ Recomendaciones Preventivas:</strong>
#                 <ul>
#                     <li>Mantener seguimiento cardiológico anual</li>
#                     <li>Dieta saludable baja en grasas saturadas</li>
#                     <li>Ejercicio regular (150 min/semana mínimo)</li>
#                     <li>Control periódico de presión arterial y colesterol</li>
#                     <li>Evitar tabaco y reducir consumo de alcohol</li>
#                 </ul>
#             </div>
#             """, unsafe_allow_html=True)
    
#     else:
#         st.info("👈 Complete los datos del paciente en el panel lateral y presione **'ANALIZAR RIESGO CARDÍACO'** para ver los resultados.")
        
#         # Mostrar información de bienvenida
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             st.markdown("""
#             ### 🏥 Para Centros Médicos
#             Sistema diseñado para integración en flujos de trabajo clínico, permitiendo evaluaciones rápidas y precisas.
#             """)
        
#         with col2:
#             st.markdown("""
#             ### 👨‍⚕️ Para Cardiólogos
#             Herramienta de apoyo diagnóstico basada en Regresión Logística con umbral optimizado (40%).
#             """)
        
#         with col3:
#             st.markdown("""
#             ### 📊 Análisis Basado en Evidencia
#             Predicciones fundamentadas en 7 variables clínicas clave (12 features con encoding).
#             """)

# with tab2:
#     if analizar:
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("🎯 Medidor de Riesgo")
#             fig_gauge = crear_gauge_chart(probabilidad)
#             st.plotly_chart(fig_gauge, use_container_width=True)
        
#         with col2:
#             st.subheader("🕸️ Análisis de Factores")
#             fig_radar = crear_radar_chart(datos_paciente)
#             st.plotly_chart(fig_radar, use_container_width=True)
        
#         # Tabla de resumen
#         st.subheader("📋 Resumen de Parámetros")
        
#         df_resumen = pd.DataFrame({
#             'Parámetro': [
#                 'Edad',
#                 'Sexo',
#                 'Frecuencia Cardíaca Máxima',
#                 'Glucosa en Ayunas',
#                 'Angina por Ejercicio',
#                 'Tipo de Dolor Torácico',
#                 'Pendiente del Segmento ST'
#             ],
#             'Valor': [
#                 f"{age} años",
#                 sex,
#                 f"{max_hr} bpm",
#                 "Sí (>120 mg/dl)" if fasting_bs == 1 else "No (<120 mg/dl)",
#                 exercise_angina,
#                 {
#                     "ASY": "Asintomático",
#                     "ATA": "Angina Atípica",
#                     "NAP": "Dolor No Anginoso",
#                     "TA": "Angina Típica"
#                 }[chest_pain_type],
#                 {
#                     "Flat": "Plana",
#                     "Up": "Ascendente",
#                     "Down": "Descendente"
#                 }[st_slope]
#             ],
#             'Estado': [
#                 '⚠️ Riesgo' if age > 60 else '✓ Normal',
#                 '-',
#                 '⚠️ Baja' if max_hr < (220 - age) * 0.6 else '✓ Adecuada',
#                 '⚠️ Elevada' if fasting_bs == 1 else '✓ Normal',
#                 '⚠️ Presente' if exercise_angina == "Sí" else '✓ Ausente',
#                 '⚠️ Alto Riesgo' if chest_pain_type == "ASY" else '⚠️ Moderado' if chest_pain_type in ["TA", "ATA"] else '✓ Bajo',
#                 '⚠️ Anormal' if st_slope in ["Flat", "Down"] else '✓ Normal'
#             ]
#         })
        
#         st.dataframe(df_resumen.reset_index(drop=True), use_container_width=True)
        
#     else:
#         st.info("Complete los datos del paciente para ver las visualizaciones.")

# with tab3:
#     st.subheader("📖 Información sobre Variables Clínicas")
    
#     with st.expander("📅 **Edad (Age)**"):
#         st.write("""
#         - **Descripción**: Edad del paciente en años
#         - **Importancia**: Factor de riesgo independiente. El riesgo cardiovascular aumenta con la edad
#         - **Valores de referencia**: Riesgo aumenta significativamente >55 años en hombres, >65 en mujeres
#         - **Escalado**: Esta variable SE ESCALA en el modelo (StandardScaler)
#         """)
    
#     with st.expander("👤 **Sexo (Sex)**"):
#         st.write("""
#         - **Descripción**: Sexo biológico del paciente
#         - **Importancia**: Los hombres tienen mayor riesgo cardiovascular a edades más tempranas
#         - **Diferencias**: El riesgo en mujeres aumenta después de la menopausia
#         - **Codificación**: Masculino = 1, Femenino = 0
#         """)
    
#     with st.expander("❤️ **Frecuencia Cardíaca Máxima (MaxHR)**"):
#         st.write("""
#         - **Descripción**: Frecuencia cardíaca máxima alcanzada durante prueba de esfuerzo
#         - **Importancia**: Indicador de capacidad cardiovascular
#         - **Valores de referencia**: FC máxima teórica = 220 - edad
#         - Una FC máxima baja puede indicar limitación cardiovascular
#         - **Escalado**: Esta variable SE ESCALA en el modelo (StandardScaler)
#         """)
    
#     with st.expander("🍬 **Glucosa en Ayunas (FastingBS)**"):
#         st.write("""
#         - **Descripción**: Indica si la glucosa en ayunas supera 120 mg/dl
#         - **Importancia**: La diabetes es un factor de riesgo cardiovascular mayor
#         - **Valores de referencia**:
#             - Normal: <100 mg/dl
#             - Prediabetes: 100-125 mg/dl
#             - Diabetes: ≥126 mg/dl
#         - **Codificación**: 0 = No (≤120), 1 = Sí (>120)
#         """)
    
#     with st.expander("💔 **Angina Inducida por Ejercicio (ExerciseAngina)**"):
#         st.write("""
#         - **Descripción**: Presencia de dolor torácico durante actividad física
#         - **Importancia**: Síntoma cardinal de isquemia miocárdica
#         - **Significado clínico**: Sugiere obstrucción coronaria significativa
#         - **Codificación**: 0 = No, 1 = Sí
#         """)
    
#     with st.expander("🫀 **Tipo de Dolor Torácico (ChestPainType)**"):
#         st.write("""
#         - **Descripción**: Clasificación del tipo de dolor torácico reportado
#         - **Tipos**:
#             - **ASY (Asintomático)**: Sin dolor torácico - paradójicamente puede indicar mayor riesgo
#             - **TA (Angina Típica)**: Dolor torácico clásico, opresivo, relacionado con esfuerzo
#             - **ATA (Angina Atípica)**: Dolor con características no clásicas
#             - **NAP (Dolor No Anginoso)**: Dolor torácico de origen no cardíaco
#         - **Importancia**: Ayuda a determinar el origen y severidad del problema cardíaco
#         - **Codificación**: One-Hot Encoding (CP_ASY, CP_ATA, CP_NAP, CP_TA)
#         """)
    
#     with st.expander("📉 **Pendiente del Segmento ST (ST_Slope)**"):
#         st.write("""
#         - **Descripción**: Morfología de la pendiente del segmento ST en ECG de esfuerzo
#         - **Tipos**:
#             - **Up (Ascendente)**: Generalmente normal, bajo riesgo
#             - **Flat (Plana)**: Puede indicar isquemia, riesgo moderado-alto
#             - **Down (Descendente)**: Fuertemente sugestivo de isquemia, alto riesgo
#         - **Importancia**: Uno de los hallazgos más importantes en pruebas de esfuerzo
#         - **Significado**: Refleja la respuesta del corazón al ejercicio y posible isquemia
#         - **Codificación**: One-Hot Encoding (ST_Slope_Up, ST_Slope_Flat, ST_Slope_Down)
#         """)
    
#     # st.markdown("---")
    
#     # st.subheader("🤖 Información del Modelo")
#     # st.info("""
#     # **Modelo Utilizado**: Regresión Logística
    
#     # **Umbral de Clasificación**: 40% (optimizado para maximizar sensibilidad)
#     # - Probabilidad ≥ 40% → Alto Riesgo
#     # - Probabilidad < 40% → Bajo Riesgo
    
#     # **Preprocesamiento**:
#     # - Variables escaladas: Age, MaxHR (StandardScaler)
#     # - Variables binarias: Sex, FastingBS, ExerciseAngina (sin escalar)
#     # - Variables categóricas: ChestPainType, ST_Slope (One-Hot Encoding)
    
#     # **Total Features**: 12 (tras encoding)
#     # """)
    
#     st.markdown("---")
#     st.info("⚕️ **Nota Médica**: Este sistema es una herramienta de apoyo diagnóstico. Las decisiones clínicas finales deben ser tomadas por profesionales médicos cualificados considerando el contexto completo del paciente.")

# # =====================================================================
# # FOOTER
# # =====================================================================
# st.markdown("---")
# st.markdown("""
# <div class="footer">
#     <p><strong>CardioPredict Pro</strong> | Sistema de Predicción de Enfermedad Cardíaca</p>
#     <p><em>Uso exclusivo para profesionales de la salud. No sustituye el diagnóstico médico profesional.</em></p>
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import joblib
import os
import json
from sklearn.preprocessing import StandardScaler
from streamlit_lottie import st_lottie

# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="CardioPredict Pro | Sistema de Predicción Cardíaca",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# FUNCIÓN PARA CARGAR ANIMACIÓN LOTTIE
# =====================================================================
def load_lottiefile(filepath: str):
    """Carga una animación Lottie desde un archivo JSON local."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# =====================================================================
# ESTILOS CSS PERSONALIZADOS
# =====================================================================
st.markdown("""
<style>
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Estilos generales */
    .main {
        background-color: #F5F5F5;
        font-family: 'Inter', sans-serif;
    }
    
    /* Ocultar padding superior de Streamlit */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Header personalizado */
    .custom-header {
        background: linear-gradient(135deg, #1A1A1A 0%, #2C2C2C 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .header-text h1 {
        color:#E63946;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-text p {
        color: #CCCCCC;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #E63946;
        margin-bottom: 1rem;
    }
    
    .metric-card h3 {
        color: #1A1A1A;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: #E63946;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .metric-card .value-text {
        color: #E63946;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    /* Panel de resultados */
    .risk-high {
        background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #06D6A0 0%, #05B389 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
    }
    
    .risk-high h2, .risk-low h2 {
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    
    .risk-high p, .risk-low p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Botón principal */
    .stButton > button {
        background: linear-gradient(135deg, #E63946 0%, #C92A35 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(230, 57, 70, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(230, 57, 70, 0.4);
    }
    
    /* Info boxes */
    .info-box {
        background: #FFF4E6;
        border-left: 4px solid #FF9500;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFE5E5;
        border-left: 4px solid #E63946;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666666;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    /* Eliminar espacios entre columnas en el header */
    [data-testid="column"]:has(iframe) {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================================
# FUNCIONES AUXILIARES
# =====================================================================

@st.cache_resource
def cargar_modelo():
    """
    Carga el modelo entrenado y el scaler.
    Busca en la carpeta 'models' los archivos .pkl
    """
    try:
        modelo = joblib.load('models/modelo_coronario.pkl')
        scaler = joblib.load('models/scaler_coronario.pkl')
        return modelo, scaler, True
    except FileNotFoundError:
        st.error("⚠️ No se encontraron los archivos del modelo. Asegúrate de tener la carpeta 'models' con los archivos 'modelo_coronario.pkl' y 'scaler_coronario.pkl'")
        return None, None, False

def preparar_datos_para_prediccion(datos, scaler):
    """
    Prepara los datos del paciente en el formato correcto para el modelo.
    """
    # Crear las columnas one-hot para ChestPainType
    cp_asy = 1 if datos['chest_pain_type'] == 'ASY' else 0
    cp_ata = 1 if datos['chest_pain_type'] == 'ATA' else 0
    cp_nap = 1 if datos['chest_pain_type'] == 'NAP' else 0
    cp_ta = 1 if datos['chest_pain_type'] == 'TA' else 0
    
    # Crear las columnas one-hot para ST_Slope
    st_slope_flat = 1 if datos['st_slope'] == 'Flat' else 0
    st_slope_up = 1 if datos['st_slope'] == 'Up' else 0
    st_slope_down = 1 if datos['st_slope'] == 'Down' else 0
    
    # ExerciseAngina convertido a binario
    exercise_angina_bin = 1 if datos['exercise_angina'] == "Sí" else 0
    
    # Crear DataFrame
    X = pd.DataFrame([[
        datos['age'], datos['sex'], datos['max_hr'], datos['fasting_bs'],
        exercise_angina_bin, cp_asy, cp_ata, cp_nap, cp_ta,
        st_slope_flat, st_slope_up, st_slope_down
    ]], columns=[
        'Age', 'Sex', 'MaxHR', 'FastingBS', 'ExerciseAngina',
        'CP_ASY', 'CP_ATA', 'CP_NAP', 'CP_TA',
        'ST_Slope_Flat', 'ST_Slope_Up', 'ST_Slope_Down'
    ])
    
    # Aplicar escalado SOLO a Age y MaxHR
    X_scaled = X.copy()
    cols_para_escalar = ['Age', 'MaxHR']
    X_scaled[cols_para_escalar] = scaler.transform(X[cols_para_escalar])
    
    return X_scaled

def predecir_riesgo(datos, modelo, scaler):
    """Realiza la predicción de riesgo cardíaco"""
    if modelo is None or scaler is None:
        return 0, "Sin modelo", [0, 0]
    
    X_preparado = preparar_datos_para_prediccion(datos, scaler)
    probabilidades = modelo.predict_proba(X_preparado)[0]
    probabilidad_enfermedad = probabilidades[1] * 100
    clasificacion = "Alto Riesgo" if probabilidad_enfermedad >= 40 else "Bajo Riesgo"
    
    return probabilidad_enfermedad, clasificacion, probabilidades

def crear_gauge_chart(probabilidad):
    """Crea un medidor visual del riesgo"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probabilidad,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Nivel de Riesgo (%)", 'font': {'size': 24, 'color': '#1A1A1A'}},
        delta={'reference': 40, 'increasing': {'color': "#E63946"}, 'decreasing': {'color': "#06D6A0"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#1A1A1A"},
            'bar': {'color': "#E63946" if probabilidad >= 40 else "#06D6A0"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E0E0E0",
            'steps': [
                {'range': [0, 40], 'color': '#E8F5E9'},
                {'range': [40, 70], 'color': '#FFF4E6'},
                {'range': [70, 100], 'color': '#FFE5E5'}
            ],
            'threshold': {
                'line': {'color': "#E63946", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="white",
        font={'color': "#1A1A1A", 'family': "Inter"},
        height=350
    )
    
    return fig

def crear_radar_chart(datos):
    """Crea un gráfico de radar con los factores de riesgo"""
    categorias = ['Edad', 'Frec. Cardíaca', 'Glucosa', 'Tipo Dolor', 'Angina', 'Pendiente ST']
    
    valores = [
        min((datos['age'] / 100) * 100, 100),
        min((datos['max_hr'] / 200) * 100, 100),
        datos['fasting_bs'] * 100,
        {'ASY': 100, 'TA': 75, 'ATA': 50, 'NAP': 25}[datos['chest_pain_type']],
        100 if datos['exercise_angina'] == "Sí" else 0,
        {'Flat': 100, 'Down': 75, 'Up': 25}[datos['st_slope']]
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(230, 57, 70, 0.3)',
        line=dict(color='#E63946', width=2),
        name='Factores del Paciente'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#E0E0E0'),
            bgcolor='white'
        ),
        showlegend=False,
        paper_bgcolor='white',
        font={'color': "#1A1A1A", 'family': "Inter"},
        height=400
    )
    
    return fig

# =====================================================================
# CARGAR MODELO Y ANIMACIÓN
# =====================================================================
modelo, scaler, modelo_cargado = cargar_modelo()
lottie_heart = load_lottiefile("./assets/Heart with ECG.json")

# =====================================================================
# HEADER CON ANIMACIÓN LOTTIE
# =====================================================================
# Crear contenedor centrado
st.markdown("""
<div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
</div>
""", unsafe_allow_html=True)

# Columnas para centrar el contenido
col_anim, col_text = st.columns([2, 3])

with col_anim:
    if lottie_heart:
        st_lottie(lottie_heart, height=350, key="header_heart", quality="high", speed=1)
    else:
        st.markdown("<div style='font-size: 12rem; text-align: center; line-height: 1;'>❤️</div>", unsafe_allow_html=True)

with col_text:
    st.markdown("""
    <div style="display: flex; flex-direction: column; justify-content: center; height: 250px;">
        <h1 style="color: #DC143C; font-size: 4rem; font-weight: 700; margin: 0; line-height: 1.2;">
            CardioPredict Pro
        </h1>
        <p style="color: #666666; font-size: 1.2rem; margin-top: 1rem; margin-bottom: 0; line-height: 1.4;">
            Sistema Inteligente de Evaluación de Riesgo Cardiovascular
        </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================================
# VERIFICAR MODELO
# =====================================================================
if not modelo_cargado:
    st.warning("""
    ### 📁 Instrucciones para cargar el modelo:
    
    1. Crea una carpeta llamada `models` en el mismo directorio que esta aplicación
    2. Coloca los siguientes archivos dentro de la carpeta `models`:
       - `modelo_coronario.pkl` (tu modelo entrenado)
       - `scaler_coronario.pkl` (tu scaler entrenado)
    3. Coloca tu animación Lottie en `./assets/Heart with ECG.json`
    4. Recarga la aplicación
    """)
    st.stop()

# =====================================================================
# SIDEBAR - ENTRADA DE DATOS
# =====================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913133.png", width=100)
    st.title("📋 Datos del Paciente")
    st.markdown("---")
    
    st.subheader("🆔 Información General")
    patient_id = st.text_input("ID del Paciente", placeholder="Ej: PAC-2024-001")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Edad", min_value=1, max_value=120, value=50, step=1)
    with col2:
        sex = st.selectbox("Sexo", ["Masculino", "Femenino"])
    
    st.markdown("---")
    st.subheader("🔬 Parámetros Cardíacos")
    
    max_hr = st.number_input(
        "Frecuencia Cardíaca Máxima (bpm)",
        min_value=60, max_value=220, value=150, step=1,
        help="Frecuencia cardíaca máxima alcanzada durante ejercicio"
    )
    
    fasting_bs = st.selectbox(
        "Glucosa en Ayunas > 120 mg/dl",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Sí",
        help="Indica si la glucosa en ayunas supera los 120 mg/dl"
    )
    
    st.markdown("---")
    st.subheader("💔 Síntomas y ECG")
    
    exercise_angina = st.selectbox(
        "Angina Inducida por Ejercicio",
        ["No", "Sí"],
        help="Dolor torácico durante actividad física"
    )
    
    chest_pain_type = st.selectbox(
        "Tipo de Dolor Torácico",
        ["ASY", "ATA", "NAP", "TA"],
        format_func=lambda x: {
            "ASY": "Asintomático",
            "ATA": "Angina Atípica",
            "NAP": "Dolor No Anginoso",
            "TA": "Angina Típica"
        }[x],
        help="Tipo de dolor en el pecho reportado por el paciente"
    )
    
    st_slope = st.selectbox(
        "Pendiente del Segmento ST",
        ["Flat", "Up", "Down"],
        format_func=lambda x: {
            "Flat": "Plana",
            "Up": "Ascendente",
            "Down": "Descendente"
        }[x],
        help="Pendiente del segmento ST en el electrocardiograma de esfuerzo"
    )
    
    st.markdown("---")
    analizar = st.button("🔍 ANALIZAR RIESGO CARDÍACO", use_container_width=True)
    
    st.markdown("---")
    st.caption("⚕️ Desarrollado para profesionales médicos")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.caption("🤖 Modelo: Regresión Logística")

# =====================================================================
# CONTENIDO PRINCIPAL
# =====================================================================
tab1, tab2, tab3 = st.tabs(["📊 Análisis de Riesgo", "📈 Visualizaciones", "ℹ️ Información Médica"])

with tab1:
    if analizar:
        datos_paciente = {
            'age': age,
            'sex': 1 if sex == "Masculino" else 0,
            'max_hr': max_hr,
            'fasting_bs': fasting_bs,
            'exercise_angina': exercise_angina,
            'chest_pain_type': chest_pain_type,
            'st_slope': st_slope
        }
        
        probabilidad, clasificacion, probs = predecir_riesgo(datos_paciente, modelo, scaler)
        
        if clasificacion == "Alto Riesgo":
            st.markdown(f"""
            <div class="risk-high">
                <h2>⚠️ ALTO RIESGO DETECTADO</h2>
                <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="risk-low">
                <h2>✓ RIESGO BAJO</h2>
                <p>Probabilidad de enfermedad cardíaca: {probabilidad:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅 Edad</h3>
                <div class="value">{age}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>❤️ FC Máxima</h3>
                <div class="value">{max_hr}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            dolor_texto = {
                "ASY": "Asintomático",
                "ATA": "Ang. Atípica",
                "NAP": "No Anginoso",
                "TA": "Ang. Típica"
            }[chest_pain_type]
            st.markdown(f"""
            <div class="metric-card">
                <h3>💔 Tipo Dolor</h3>
                <div class="value-text">{dolor_texto}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            slope_texto = {
                "Flat": "Plana",
                "Up": "Ascendente",
                "Down": "Descendente"
            }[st_slope]
            st.markdown(f"""
            <div class="metric-card">
                <h3>📉 Pendiente ST</h3>
                <div class="value-text">{slope_texto}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probabilidad Sin Enfermedad", f"{probs[0]*100:.1f}%")
        with col2:
            st.metric("Probabilidad Con Enfermedad", f"{probs[1]*100:.1f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Recomendaciones Médicas")
        
        if clasificacion == "Alto Riesgo":
            st.markdown("""
            <div class="warning-box">
                <strong>⚠️ Acciones Recomendadas:</strong>
                <ul>
                    <li>Evaluación cardiológica completa de forma urgente</li>
                    <li>Electrocardiograma de 12 derivaciones</li>
                    <li>Ecocardiograma y prueba de esfuerzo supervisada</li>
                    <li>Analítica completa incluyendo perfil lipídico</li>
                    <li>Considerar derivación a unidad de cardiología</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <strong>✓ Recomendaciones Preventivas:</strong>
                <ul>
                    <li>Mantener seguimiento cardiológico anual</li>
                    <li>Dieta saludable baja en grasas saturadas</li>
                    <li>Ejercicio regular (150 min/semana mínimo)</li>
                    <li>Control periódico de presión arterial y colesterol</li>
                    <li>Evitar tabaco y reducir consumo de alcohol</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Complete los datos del paciente en el panel lateral y presione **'ANALIZAR RIESGO CARDÍACO'** para ver los resultados.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 🏥 Para Centros Médicos
            Sistema diseñado para integración en flujos de trabajo clínico, permitiendo evaluaciones rápidas y precisas.
            """)
        
        with col2:
            st.markdown("""
            ### 👨‍⚕️ Para Cardiólogos
            Herramienta de apoyo diagnóstico basada en Regresión Logística con umbral optimizado (40%).
            """)
        
        with col3:
            st.markdown("""
            ### 📊 Análisis Basado en Evidencia
            Predicciones fundamentadas en 7 variables clínicas clave (12 features con encoding).
            """)

with tab2:
    if analizar:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Medidor de Riesgo")
            fig_gauge = crear_gauge_chart(probabilidad)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.subheader("🕸️ Análisis de Factores")
            fig_radar = crear_radar_chart(datos_paciente)
            st.plotly_chart(fig_radar, use_container_width=True)
        
        st.subheader("Resumen de Parámetros")
        
        tipo_dolor_texto = {'ASY': 'Asintomático', 'ATA': 'Angina Atípica', 'NAP': 'Dolor No Anginoso', 'TA': 'Angina Típica'}[chest_pain_type]
        pendiente_texto = {'Flat': 'Plana', 'Up': 'Ascendente', 'Down': 'Descendente'}[st_slope]
       # Crear tabla HTML personalizada en lugar de st.dataframe
        tabla_html = f"""
        <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden;">
           <thead>
              <tr style="background: #F5F5F5;">
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Parámetro</th>
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Valor</th>
                   <th style="padding: 1rem; text-align: left; border-bottom: 2px solid #E0E0E0;">Estado</th>
              </tr>
            </thead>
            <tbody>
               <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Edad</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{age} años</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Riesgo' if age > 60 else '✓ Normal'}</td>
               </tr>
               <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Sexo</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{sex}</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">-</td>
              </tr>
              <tr>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Frecuencia Cardíaca Máxima</td>
                   <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{max_hr} bpm</td>
                <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Baja' if max_hr < (220 - age) * 0.6 else '✓ Adecuada'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Glucosa en Ayunas</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{"Sí (>120 mg/dl)" if fasting_bs == 1 else "No (<120 mg/dl)"}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Elevada' if fasting_bs == 1 else '✓ Normal'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Angina por Ejercicio</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{exercise_angina}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Presente' if exercise_angina == "Sí" else '✓ Ausente'}</td>
              </tr>
              <tr>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">Tipo de Dolor Torácico</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{tipo_dolor_texto}</td>
                  <td style="padding: 1rem; border-bottom: 1px solid #F0F0F0;">{'⚠️ Alto Riesgo' if chest_pain_type == "ASY" else '⚠️ Moderado' if chest_pain_type in ["TA", "ATA"] else '✓ Bajo'}</td>
              </tr>
              <tr>
                 <td style="padding: 1rem;">Pendiente del Segmento ST</td>
                 <td style="padding: 1rem;">{pendiente_texto}</td>
                 <td style="padding: 1rem;">{'⚠️ Anormal' if st_slope in ["Flat", "Down"] else '✓ Normal'}</td>
              </tr>
            </tbody>
        </table>
        """

        st.markdown(tabla_html, unsafe_allow_html=True)
    else:
        st.info("Complete los datos del paciente para ver las visualizaciones.")

with tab3:
    st.subheader("📖 Información sobre Variables Clínicas")
    
    with st.expander("📅 **Edad (Age)**"):
        st.write("Factor de riesgo independiente. Riesgo aumenta >55 años (hombres), >65 años (mujeres)")
    
    with st.expander("❤️ **Frecuencia Cardíaca Máxima (MaxHR)**"):
        st.write("FC máxima teórica = 220 - edad. Una FC baja indica limitación cardiovascular")
    
    with st.expander("🍬 **Glucosa en Ayunas (FastingBS)**"):
        st.write("0 = ≤120 mg/dl, 1 = >120 mg/dl")
        st.write("La diabetes es un factor de riesgo cardiovascular mayor")
    
    with st.expander("💔 **Angina por Ejercicio (ExerciseAngina)**"):
        st.write("Síntoma cardinal de isquemia miocárdica. Sugiere obstrucción coronaria")
    
    with st.expander("🫀 **Tipo de Dolor Torácico (ChestPainType)**"):
        st.write("**ASY**: Asintomático - paradójicamente mayor riesgo")
        st.write("**TA**: Angina Típica - dolor clásico")
        st.write("**ATA**: Angina Atípica")
        st.write("**NAP**: Dolor No Anginoso")
    
    with st.expander("📉 **Pendiente ST (ST_Slope)**"):
        st.write("**Up**: Normal, bajo riesgo")
        st.write("**Flat**: Isquemia, riesgo moderado-alto")
        st.write("**Down**: Isquemia severa, alto riesgo")
    
    st.markdown("---")
    st.info("⚕️ **Nota Médica**: Este sistema es una herramienta de apoyo diagnóstico. Las decisiones clínicas finales deben ser tomadas por profesionales médicos cualificados.")

