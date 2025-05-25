import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general del dashboard
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Dashboard de Ventas")

# Cargar los datos
df = pd.read_excel("retail_limpio.xlsx")
df = pd.read_excel("retail_limpio.xlsx")

# Aquí va el nuevo filtro de país
paises_disponibles = df["País/Región"].unique()
pais_seleccionado = st.sidebar.selectbox("Selecciona el país", sorted(paises_disponibles))
df = df[df["País/Región"] == pais_seleccionado]



# Procesar fechas
df["Fecha del pedido"] = pd.to_datetime(df["Fecha del pedido"])
df["año_pedido"] = df["Fecha del pedido"].dt.year
df["mes_pedido"] = df["Fecha del pedido"].dt.month

# Filtro 2: Año
años_disponibles = sorted(df["año_pedido"].unique())
año_seleccionado = st.sidebar.multiselect("📅 Filtra por año(s)", años_disponibles, default=años_disponibles)
df = df[df["año_pedido"].isin(año_seleccionado)]

# Filtro 3: Categoría (opcional)
categorias_disponibles = sorted(df["Categoría"].unique())
categoria_seleccionada = st.sidebar.multiselect("📦 Filtra por categoría(s)", categorias_disponibles, default=categorias_disponibles)
df = df[df["Categoría"].isin(categoria_seleccionada)]

# 🔎 Mostrar los filtros aplicados directamente en el dashboard
st.markdown(f"**📍 País seleccionado:** `{pais_seleccionado}`")
st.markdown(f"**🗓️ Años seleccionados:** `{', '.join(map(str, año_seleccionado))}`")
st.markdown(f"**📦 Categorías seleccionadas:** `{', '.join(categoria_seleccionada)}`")

# KPIs destacados
ventas_totales = df["Ventas"].sum()
ganancias_totales = df["Ganancia"].sum()
fecha_max_ventas = df.groupby(["año_pedido", "mes_pedido"])["Ventas"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas Totales", f"${ventas_totales:,.0f}")
col2.metric("📈 Ganancias Totales", f"${ganancias_totales:,.0f}")
col3.metric("📅 Mes Pico de Ventas", f"{fecha_max_ventas[1]}/{fecha_max_ventas[0]}")

# === Ventas por categoría ===
st.subheader("📦 Ventas Totales por Categoría de Producto")

ventas_categoria = df.groupby("Categoría")["Ventas"].sum().sort_values(ascending=False)

fig1, ax1 = plt.subplots(figsize=(5, 3), constrained_layout=True)  # más pequeño y limpio
ventas_categoria.plot(kind="bar", ax=ax1, color="steelblue")

ax1.set_ylabel("Ventas", fontsize=10)
ax1.set_xlabel("Categoría", fontsize=10)
ax1.set_title("Ventas Totales por Categoría", fontsize=12)
ax1.tick_params(axis='x', rotation=0, labelsize=9)

fig1.tight_layout()  # evita que se desborde

st.pyplot(fig1)

st.subheader("📅 Evolución Mensual de Ventas y Ganancias")

# Agrupamos por año y mes para obtener ventas y ganancias mensuales
ventas_mensuales = df.groupby(["año_pedido", "mes_pedido"])[["Ventas", "Ganancia"]].sum().reset_index()

# Creamos una columna de fecha real para facilitar la gráfica
ventas_mensuales["Fecha"] = pd.to_datetime(
    ventas_mensuales["año_pedido"].astype(str) + "-" + ventas_mensuales["mes_pedido"].astype(str) + "-01"
)

# Graficamos con matplotlib
fig2, ax2 = plt.subplots(figsize=(8, 4))
ax2.plot(ventas_mensuales["Fecha"], ventas_mensuales["Ventas"], label="Ventas", color="royalblue", marker="o")
ax2.plot(ventas_mensuales["Fecha"], ventas_mensuales["Ganancia"], label="Ganancia", color="forestgreen", marker="s")

ax2.set_title("Ventas y Ganancias Mensuales")
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Valor ($)")
ax2.legend()
ax2.grid(True)

fig2.tight_layout()
st.pyplot(fig2)

st.subheader("🌎 Top 10 Departamentos/Ptovincias por Ventas Totales")

# Agrupamos por departamento
ventas_departamento = df.groupby("Provincia/Estado/Departamento")["Ventas"].sum().sort_values(ascending=False).head(10)

# Graficamos horizontalmente
fig3, ax3 = plt.subplots(figsize=(8, 5))
ventas_departamento.plot(kind="barh", ax=ax3, color="skyblue")

ax3.set_xlabel("Ventas")
ax3.set_ylabel("Departamento")
ax3.set_title("Top 10 departamentos por ventas totales")
ax3.invert_yaxis()  # Muestra el más alto arriba

fig3.tight_layout()
st.pyplot(fig3)

st.subheader("🧑‍🤝‍🧑 Ventas Totales por Segmento de Cliente")

ventas_segmento = df.groupby("Segmento")["Ventas"].sum().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(6, 4))
ventas_segmento.plot(kind="bar", ax=ax4, color="lightcoral")

ax4.set_ylabel("Ventas")
ax4.set_xlabel("Segmento")
ax4.set_title("Ventas Totales por Segmento de Cliente")
fig4.tight_layout()
st.pyplot(fig4)

st.subheader("🧾 Top 5 Subcategorías Más Vendidas")

ventas_subcat = df.groupby("Subcategoría")["Ventas"].sum().sort_values(ascending=False).head(5)

fig5, ax5 = plt.subplots(figsize=(6, 4))
ventas_subcat.plot(kind="bar", ax=ax5, color="goldenrod")

ax5.set_ylabel("Ventas")
ax5.set_xlabel("Subcategoría")
ax5.set_title("Top 5 Subcategorías por Ventas Totales")
fig5.tight_layout()
st.pyplot(fig5)

# === Conclusiones dinámicas ===
st.subheader("📌 Conclusiones según los filtros seleccionados")

# Categoría más vendida
categoria_top = df.groupby("Categoría")["Ventas"].sum().idxmax()

# Subcategoría más vendida
subcat_top = df.groupby("Subcategoría")["Ventas"].sum().idxmax()

# Segmento más comprador
segmento_top = df.groupby("Segmento")["Ventas"].sum().idxmax()

# Método de envío más usado
envio_top = df.groupby("Método de envío")["Ventas"].sum().idxmax()

# Mes pico de ventas
fecha_pico = df.groupby(["año_pedido", "mes_pedido"])["Ventas"].sum().idxmax()
mes_pico = f"{fecha_pico[1]:02}/{fecha_pico[0]}"

# Departamento top ventas
depto_top = df.groupby("Provincia/Estado/Departamento")["Ventas"].sum().idxmax()

# Mostrar en panel markdown
st.markdown(f"""
- 📦 La **categoría más vendida** es: `{categoria_top}`
- 🧾 La **subcategoría más vendida** es: `{subcat_top}`
- 🧍‍♂️ El **segmento que más compra** es: `{segmento_top}`
- 📦 El **método de envío más usado** es: `{envio_top}`
- 📅 El **mes pico de ventas** fue: `{mes_pico}`
- 🗺️ El **departamento con más ventas** es: `{depto_top}`

Estas métricas te permiten tomar decisiones más precisas y enfocadas para campañas de marketing.
""")

