import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Cajun Industries - Field Calc", layout="centered")

# Estilo visual (Colores de la empresa)
st.markdown("""
    <style>
    .main { background-color: #B6D7E2; }
    .stButton>button { background-color: #23345C; color: white; width: 100%; border-radius: 10px; height: 3em; font-size: 18px; }
    .result-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-left: 5px solid #1D5336; }
    </style>
    """, unsafe_allow_contents=True)

st.title("🏗️ Cajun Industries")
st.subheader("Field Calculators")

# Selector de herramienta
option = st.selectbox("Selecciona una calculadora:", ["Excavation", "Concrete"])

if option == "Excavation":
    st.write("### Excavation Layout Inputs")
    
    col1, col2 = st.columns(2)
    with col1:
        bm = st.number_input("BM (Benchmark) [ft]", value=0.0, format="%.2f")
        rr = st.number_input("RR (Backsight) [ft]", value=0.0, format="%.2f")
        elev_a = st.number_input("Elevation at A [ft]", value=0.0, format="%.2f")
    with col2:
        elev_b = st.number_input("Elevation at B [ft]", value=0.0, format="%.2f")
        distancia = st.number_input("Distance A to B [ft]", value=1.0, format="%.2f")
        tramo = st.number_input("Segment Length [ft]", value=1.0, format="%.2f")
    
    offset = st.number_input("SS/Stone Height [ft]", value=0.0, format="%.2f")

    if st.button("CALCULATE"):
        if distancia <= 0 or tramo <= 0:
            st.error("Error: La distancia y el tramo deben ser mayores a cero.")
        else:
            # Lógica de cálculo (Tu código original)
            hi = bm + rr
            slope = (elev_a - elev_b) / distancia
            slope_pct = slope * 100
            rod_reading_a = hi - elev_a

            # Generar segmentos
            dists = []
            d = 0.0
            while d < distancia:
                dists.append(round(d, 2))
                d += tramo
            if dists[-1] != round(distancia, 2):
                dists.append(round(distancia, 2))

            # Crear tabla de resultados
            data = []
            for idx, d_val in enumerate(dists):
                ss = rod_reading_a + (slope * d_val)
                tod = ss + offset
                data.append([idx, d_val, round(ss, 2), round(tod, 2)])

            df = pd.DataFrame(data, columns=["No.", "Dist (ft)", "SS (ft)", "TOD (ft)"])

            # Mostrar Resultados Generales
            st.success("Cálculo Completado")
            c1, c2 = st.columns(2)
            c1.metric("HI (Inst. Height)", f"{hi:.2f} ft")
            c2.metric("Slope (%)", f"{slope_pct:.2f}%")
            
            # Mostrar Tabla
            st.write("### Rod Readings")
            st.dataframe(df, use_container_width=True)

            # Preparar archivo para descargar
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            reporte = f"Cajun Industries Report - {now}\n" + df.to_string(index=False)
            
            st.download_button(
                label="📥 Descargar Resultados (.txt)",
                data=reporte,
                file_name=f"excavation_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

elif option == "Concrete":
    st.info("Calculadora de concreto en desarrollo...")
