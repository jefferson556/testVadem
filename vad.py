import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Cargar datos ---
@st.cache_data
def cargar_datos():
    df = pd.read_excel("pagina.xlsx")

    # Limpieza de columnas
    df.columns = df.columns.str.strip()
    df["PRINCIPIO ACTIVO"] = (
        df["PRINCIPIO ACTIVO"].astype(str)
        .str.strip()
        .str.replace(r"\s*,\s*", ",", regex=True)
        .str.split()
        .str.join(" ")
        .str.upper()
    )
    df["FORMA FARMACEUTICA"] = df["FORMA FARMACEUTICA"].astype(str).str.strip().str.upper()
    df["DOSIS"] = df["DOSIS"].astype(str).str.strip().str.lower()
    return df

df = cargar_datos()

st.title("💊 Analizador de PVP de Medicamentos")

# --- Widgets de selección ---
principio = st.selectbox(
    "Selecciona Principio Activo:",
    sorted(df["PRINCIPIO ACTIVO"].unique())
)

dosis = st.selectbox(
    "Selecciona Dosis:",
    sorted(df.loc[df["PRINCIPIO ACTIVO"] == principio, "DOSIS"].unique())
)

forma = st.selectbox(
    "Selecciona Forma Farmacéutica:",
    sorted(df.loc[
        (df["PRINCIPIO ACTIVO"] == principio) & 
        (df["DOSIS"] == dosis),
        "FORMA FARMACEUTICA"
    ].unique())
)

# --- Botón para generar gráfica ---
if st.button("📊 Generar Gráfica"):
    subset = df[
        (df["PRINCIPIO ACTIVO"] == principio) &
        (df["DOSIS"] == dosis) &
        (df["FORMA FARMACEUTICA"] == forma)
    ][["NOMBRE MEDICAMENTO", "LABORATORIO", "PVP"]]

    if subset.empty:
        st.warning("⚠️ No se encontraron datos para esta combinación.")
    else:
        st.success(f"Se encontraron {len(subset)} resultados.")

        # --- Tabla de resultados ---
        st.subheader("Resultados Filtrados")
        st.dataframe(subset)

        # --- Gráfico de barras ---
        st.subheader("Comparación de PVP por Marca")
        fig, ax = plt.subplots(figsize=(10,5))
        ax.bar(subset["NOMBRE MEDICAMENTO"], subset["PVP"], color="skyblue", edgecolor="black")
        plt.xticks(rotation=45, ha="right")
        ax.set_ylabel("Precio PVP")
        ax.set_xlabel("Marca / Medicamento")
        ax.set_title(f"{principio} {dosis} - {forma}")
        st.pyplot(fig)

        # --- Gráfico de pastel ---
        st.subheader("Distribución de PVP (Pastel)")
        fig2, ax2 = plt.subplots(figsize=(6,6))
        ax2.pie(
            subset["PVP"], 
            labels=subset["NOMBRE MEDICAMENTO"], 
            autopct="%1.1f%%", 
            startangle=140,
            wedgeprops={'edgecolor': 'black'}
        )
        ax2.set_title("Distribución de PVP por Marca")
        st.pyplot(fig2)
