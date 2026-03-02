import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px


def carregar_dados():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credenciais.json",
        scopes=scope
    )

    client = gspread.authorize(creds)
    sheet = client.open("Flcx_Isaque").worksheet("db_fluxocaixa")

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    df["VALOR"] = pd.to_numeric(df["VALOR"], errors="coerce")

    return df


st.set_page_config(layout="wide")
st.title("Dashboard Financeiro")

df = carregar_dados()

# KPIs
entradas = df[df["TIPO"] == "Entrada"]["VALOR"].sum()
saidas = df[df["TIPO"] == "Saída"]["VALOR"].sum()
saldo = entradas - saidas

col1, col2, col3 = st.columns(3)

col1.metric("Entradas", f"R$ {entradas:,.2f}")
col2.metric("Saídas", f"R$ {saidas:,.2f}")
col3.metric("Saldo", f"R$ {saldo:,.2f}")

# Gráfico de gastos por categoria
df_saida = df[df["TIPO"] == "Saída"]
categoria = df_saida.groupby("CATEGORIA")["VALOR"].sum().reset_index()

fig = px.pie(categoria, names="CATEGORIA", values="VALOR", title="Gastos por Categoria")
st.plotly_chart(fig, use_container_width=True)
