import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# Configuración de la página
st.set_page_config(page_title="Taller 21 - Análisis de Ventas", layout="wide")

CSV_FILE = "ventas_comerciales.csv"

# 1. Función para inicializar la base de datos con los 25 registros si no existe
def inicializar_datos():
    if not os.path.exists(CSV_FILE):
        datos_iniciales = [
            ["V001", "2026-06-05", "Ryzen 5 5600G", "Procesadores", 4, 130, 95],
            ["V002", "2026-06-12", "Radeon RX 6600", "Tarjetas Gráficas", 3, 210, 165],
            ["V003", "2026-06-18", "SSD NVMe 1TB", "Almacenamiento", 8, 85, 52],
            ["V004", "2026-06-25", "Monitor QHD 27\"", "Monitores", 2, 260, 190],
            ["V005", "2026-07-03", "Teclado Mecánico Pro", "Periféricos", 6, 110, 60],
            ["V006", "2026-07-10", "Audífonos Wireless", "Periféricos", 10, 65, 32],
            ["V007", "2026-07-15", "Ryzen 5 7600", "Procesadores", 5, 220, 170],
            ["V008", "2026-07-22", "RAM DDR5 32GB", "Memoria", 7, 105, 68],
            ["V009", "2026-07-29", "Chasis Airflow ATX", "Componentes", 4, 95, 58],
            ["V010", "2026-08-04", "Board B650M", "Componentes", 5, 150, 110],
            ["V011", "2026-08-11", "Radeon RX 6600", "Tarjetas Gráficas", 5, 210, 165],
            ["V012", "2026-08-17", "SSD NVMe 1TB", "Almacenamiento", 12, 85, 52],
            ["V013", "2026-08-24", "Audífonos Wireless", "Periféricos", 8, 65, 32],
            ["V014", "2026-08-30", "Monitor QHD 27\"", "Monitores", 4, 260, 190],
            ["V015", "2026-09-05", "Teclado Mecánico Pro", "Periféricos", 9, 110, 60],
            ["V016", "2026-09-12", "Ryzen 5 5600G", "Procesadores", 6, 130, 95],
            ["V017", "2026-09-19", "RAM DDR5 32GB", "Memoria", 10, 105, 68],
            ["V018", "2026-09-26", "Chasis Airflow ATX", "Componentes", 6, 95, 58],
            ["V019", "2026-10-02", "Ryzen 5 7600", "Procesadores", 7, 220, 170],
            ["V020", "2026-10-09", "Board B650M", "Componentes", 7, 150, 110],
            ["V021", "2026-10-15", "Radeon RX 6600", "Tarjetas Gráficas", 6, 210, 165],
            ["V022", "2026-10-21", "Monitor QHD 27\"", "Monitores", 5, 260, 190],
            ["V023", "2026-10-28", "SSD NVMe 1TB", "Almacenamiento", 15, 85, 52],
            ["V024", "2026-11-04", "Teclado Mecánico Pro", "Periféricos", 11, 110, 60],
            ["V025", "2026-11-10", "Audífonos Wireless", "Periféricos", 14, 65, 32]
        ]
        df = pd.DataFrame(datos_iniciales, columns=[
            "ID_Venta", "Fecha", "Producto", "Categoria", "Cantidad", "Precio_Unitario", "Costo_Unitario"
        ])
        df["Ingreso_Total"] = df["Cantidad"] * df["Precio_Unitario"]
        df["Costo_Total"] = df["Cantidad"] * df["Costo_Unitario"]
        df["Utilidad"] = df["Ingreso_Total"] - df["Costo_Total"]
        df["Margen_Porcentaje"] = round((df["Utilidad"] / df["Ingreso_Total"]) * 100, 2)
        df.to_csv(CSV_FILE, index=False)

inicializar_datos()
df = pd.read_csv(CSV_FILE)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)

# Encabezado
st.title("TALLER 5 - Evidencias en un Dashboard")
st.markdown("**Autor:** David Alejandro Bonilla | **Enfoque:** Tendencias, ventas por producto y rentabilidad.")
st.divider()

# Barra lateral: Formulario de registro y Filtros
st.sidebar.header("Formulario de Nueva Venta")
with st.sidebar.form("form_venta", clear_on_submit=True):
    nueva_fecha = st.date_input("Fecha de venta", date.today())
    nuevo_prod = st.selectbox("Producto", df["Producto"].unique())
    nueva_cat = df[df["Producto"] == nuevo_prod]["Categoria"].iloc[0]
    nueva_cant = st.number_input("Cantidad vendida", min_value=1, value=1)
    nuevo_precio = st.number_input("Precio Unitario (USD)", min_value=1.0, value=float(df[df["Producto"] == nuevo_prod]["Precio_Unitario"].iloc[0]))
    nuevo_costo = st.number_input("Costo Unitario (USD)", min_value=1.0, value=float(df[df["Producto"] == nuevo_prod]["Costo_Unitario"].iloc[0]))
    submit = st.form_submit_button("Guardar Registro")

    if submit:
        nuevo_id = f"V{len(df) + 1:03d}"
        ingreso = nueva_cant * nuevo_precio
        costo = nueva_cant * nuevo_costo
        utilidad = ingreso - costo
        margen = round((utilidad / ingreso) * 100, 2)
        
        nueva_fila = pd.DataFrame([[
            nuevo_id, str(nueva_fecha), nuevo_prod, nueva_cat, nueva_cant,
            nuevo_precio, nuevo_costo, ingreso, costo, utilidad, margen
        ]], columns=df.drop(columns=["Mes"]).columns)
        
        df_actualizado = pd.concat([pd.read_csv(CSV_FILE), nueva_fila], ignore_index=True)
        df_actualizado.to_csv(CSV_FILE, index=False)
        st.sidebar.success(f"¡Venta {nuevo_id} registrada!")
        st.rerun()

# Filtros interactivos
st.sidebar.header("Filtros del Dashboard")
categorias_sel = st.sidebar.multiselect(
    "Filtrar por Categoría:",
    options=df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

df_filtrado = df[df["Categoria"].isin(categorias_sel)]

# 2. SECCIÓN DE 4 INDICADORES KPI
st.subheader("Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3, col4 = st.columns(4)

ingresos_totales = df_filtrado["Ingreso_Total"].sum()
utilidad_total = df_filtrado["Utilidad"].sum()
margen_promedio = (utilidad_total / ingresos_totales * 100) if ingresos_totales > 0 else 0
unidades_totales = df_filtrado["Cantidad"].sum()

col1.metric("Ingresos Totales (Ventas)", f"${ingresos_totales:,.2f} USD")
col2.metric("Utilidad Neta Total", f"${utilidad_total:,.2f} USD")
col3.metric("Margen de Rentabilidad", f"{margen_promedio:.2f}%")
col4.metric("Unidades Vendidas", f"{unidades_totales} uds")

st.divider()

# 3. SECCIÓN DE 3 VISUALIZACIONES GRÁFICAS
st.subheader("Visualizaciones de Tendencias, Productos y Rentabilidad")

g_col1, g_col2 = st.columns(2)

with g_col1:
    # Gráfico 1: Tendencia temporal de ventas y utilidad
    df_mensual = df_filtrado.groupby("Mes")[["Ingreso_Total", "Utilidad"]].sum().reset_index()
    fig_tendencia = px.line(
        df_mensual, x="Mes", y=["Ingreso_Total", "Utilidad"],
        markers=True,
        title="1. Tendencia Mensual de Ingresos vs. Utilidad (USD)",
        labels={"value": "Monto (USD)", "Mes": "Mes", "variable": "Métrica"}
    )
    st.plotly_chart(fig_tendencia, use_container_width=True)

with g_col2:
    # Gráfico 2: Ventas por producto
    df_prod = df_filtrado.groupby("Producto")["Ingreso_Total"].sum().reset_index().sort_values(by="Ingreso_Total", ascending=True)
    fig_prod = px.bar(
        df_prod, x="Ingreso_Total", y="Producto", orientation="h",
        text_auto='.2s', color="Ingreso_Total", color_continuous_scale="Blues",
        title="2. Ingresos Totales por Producto (USD)"
    )
    st.plotly_chart(fig_prod, use_container_width=True)

# Gráfico 3: Rentabilidad y Margen por Producto y Categoría
df_rent = df_filtrado.groupby(["Producto", "Categoria"]).agg(
    Utilidad_Total=("Utilidad", "sum"),
    Margen_Promedio=("Margen_Porcentaje", "mean"),
    Unidades=("Cantidad", "sum")
).reset_index()

fig_rentabilidad = px.bar(
    df_rent, x="Producto", y="Utilidad_Total", color="Categoria",
    hover_data=["Margen_Promedio", "Unidades"],
    text_auto='.2s',
    title="3. Rentabilidad Neta Generada por Producto y Categoría (USD)"
)
st.plotly_chart(fig_rentabilidad, use_container_width=True)

# Tabla de base de datos
with st.expander("Ver Base de Datos Completa (Mínimo 20 registros)"):
    st.dataframe(df_filtrado.drop(columns=["Mes"]), use_container_width=True)