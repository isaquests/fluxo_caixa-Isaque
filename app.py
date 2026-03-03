import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Dashboard Financeiro")

url = "https://docs.google.com/spreadsheets/d/1n4OAhjZF3ejsU8Xl9OIKoXYdSHYPeI1SVXUHqR1UVho/export?format=csv"

df = pd.read_csv(url)

# Garantir que valor é número
df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")

# KPIs
entradas = df[df["TIPO"] == "Entrada"]["VALOR"].sum()
saidas = df[df["TIPO"] == "Saída"]["VALOR"].sum()
saldo = entradas - saidas

col1, col2, col3 = st.columns(3)

col1.metric("Entradas", f"R$ {entradas:,.2f}")
col2.metric("Saídas", f"R$ {saidas:,.2f}")
col3.metric("Saldo", f"R$ {saldo:,.2f}")

st.dataframe(df)
