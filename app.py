import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# CONFIGURAÇÃO
# ----------------------------
st.set_page_config(layout="wide")
st.title("Dashboard Financeiro")

# ----------------------------
# LEITURA DA PLANILHA
# ----------------------------
url = "https://docs.google.com/spreadsheets/d/1n4OAhjZF3ejsU8Xl9OIKoXYdSHYPeI1SVXUHqR1UVho/export?format=csv"

df = pd.read_csv(url)

# ----------------------------
# TRATAMENTO
# ----------------------------
df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")
df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")

# ----------------------------
# KPIs
# ----------------------------
entradas = df[df["TIPO"] == "Entrada"]["VALOR"].sum()
saidas = df[df["TIPO"] == "Saída"]["VALOR"].sum()
saldo = entradas - saidas

col1, col2, col3 = st.columns(3)

col1.metric("Entradas", f"R$ {entradas:,.2f}")
col2.metric("Saídas", f"R$ {saidas:,.2f}")
col3.metric("Saldo", f"R$ {saldo:,.2f}")

st.divider()

# ----------------------------
# GRÁFICO 1 - Gastos por Categoria
# ----------------------------
st.subheader("Gastos por Categoria")

df_saida = df[df["TIPO"] == "Saída"]

categoria = (
    df_saida
    .groupby("CATEGORIA")["VALOR"]
    .sum()
    .reset_index()
)

fig_pizza = px.pie(
    categoria,
    names="CATEGORIA",
    values="VALOR",
    hole=0.4
)

st.plotly_chart(fig_pizza, use_container_width=True)

st.divider()

# ----------------------------
# GRÁFICO 2 - Evolução dos Gastos
# ----------------------------
st.subheader("Evolução Mensal dos Gastos")

df_saida["MES"] = df_saida["DATA"].dt.to_period("M").astype(str)

mensal = (
    df_saida
    .groupby("MES")["VALOR"]
    .sum()
    .reset_index()
)

fig_linha = px.line(
    mensal,
    x="MES",
    y="VALOR",
    markers=True
)

st.plotly_chart(
    fig_saldo,
    use_container_width=True,
    config={
        "scrollZoom": False,
        "displayModeBar": False
    }
)

# ----------------------------
# GRÁFICO 3 - Comparação Entradas x Saídas
# ----------------------------
st.subheader("Entradas x Saídas")

comparativo = df.groupby("TIPO")["VALOR"].sum().reset_index()

fig_barra = px.bar(
    comparativo,
    x="TIPO",
    y="VALOR",
    text="VALOR",
    color="TIPO",
    color_discrete_map={
        "Entrada": "green",
        "Saída": "red"
    }
)

fig_barra.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")

st.plotly_chart(fig_barra, use_container_width=True)
