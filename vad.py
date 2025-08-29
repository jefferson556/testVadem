import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# --- Cargar archivo ---
try:
    df = pd.read_excel("pagina.xlsx")
except FileNotFoundError:
    print("Error: The file 'pagina.xlsx' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# --- Limpiar columnas ---
df.columns = df.columns.str.strip()
df["PRINCIPIO ACTIVO"] = (
    df["PRINCIPIO ACTIVO"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s*,\s*", ",", regex=True)
    .str.split()
    .str.join(" ")
    .str.upper()
)
df["FORMA FARMACEUTICA"] = df["FORMA FARMACEUTICA"].astype(str).str.strip().str.upper()
df["DOSIS"] = df["DOSIS"].astype(str).str.strip().str.lower()

# --- Funciones auxiliares ---
def get_principios(df):
    return sorted(df["PRINCIPIO ACTIVO"].dropna().unique())

def get_dosis(df, principio):
    return sorted(df.loc[df["PRINCIPIO ACTIVO"] == principio, "DOSIS"].dropna().unique())

def get_formas(df, principio, dosis):
    return sorted(df.loc[
        (df["PRINCIPIO ACTIVO"] == principio) & (df["DOSIS"] == dosis),
        "FORMA FARMACEUTICA"
    ].dropna().unique())

def graficar(df, principio, dosis, forma):
    subset = df[
        (df["PRINCIPIO ACTIVO"] == principio) &
        (df["DOSIS"] == dosis) &
        (df["FORMA FARMACEUTICA"] == forma)
    ][["NOMBRE MEDICAMENTO", "PVP"]]

    if subset.empty:
        print("⚠️ No se encontraron datos para esta combinación.")
        return

    # --- Gráfico de barras ---
    plt.figure(figsize=(12,6))
    plt.bar(subset["NOMBRE MEDICAMENTO"], subset["PVP"], color="skyblue", edgecolor="black")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Comparación de PVP - {principio} {dosis} {forma} ({len(subset)} resultados)")
    plt.ylabel("Precio PVP")
    plt.xlabel("Marca / Medicamento")

    for i, v in enumerate(subset["PVP"]):
        plt.text(i, v + 0.1, f"{v:.2f}", ha="center", fontsize=9)

    plt.tight_layout()
    plt.show()

    # --- Gráfico de pastel ---
    plt.figure(figsize=(8,8))
    plt.pie(
        subset["PVP"],
        labels=subset["NOMBRE MEDICAMENTO"],
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={'edgecolor': 'black'}
    )
    plt.title(f"Distribución de PVP - {principio} {dosis} {forma}")
    plt.show()

# --- Widgets ---
principio_dropdown = widgets.Dropdown(
    options=get_principios(df),
    description="Principio activo:",
    style={'description_width': 'initial'}
)

dosis_dropdown = widgets.Dropdown(
    options=[],
    description="Dosis:",
    style={'description_width': 'initial'}
)

forma_dropdown = widgets.Dropdown(
    options=[],
    description="Forma:",
    style={'description_width': 'initial'}
)

boton = widgets.Button(description="Generar Gráfica", button_style="success")
output = widgets.Output()

# --- Callbacks ---
def actualizar_dosis(change):
    principio = change["new"]
    dosis_dropdown.options = get_dosis(df, principio)
    forma_dropdown.options = []

def actualizar_formas(change):
    principio = principio_dropdown.value
    dosis = change["new"]
    forma_dropdown.options = get_formas(df, principio, dosis)

def generar_grafica(b):
    with output:
        clear_output()
        graficar(df, principio_dropdown.value, dosis_dropdown.value, forma_dropdown.value)

principio_dropdown.observe(actualizar_dosis, names="value")
dosis_dropdown.observe(actualizar_formas, names="value")
boton.on_click(generar_grafica)

# --- Mostrar interfaz ---
display(principio_dropdown, dosis_dropdown, forma_dropdown, boton, output)