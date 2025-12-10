import streamlit as st
import pandas as pd
from database import init, sidebar

st.title("🏆 Classificação do Bolão")

sidebar()

@st.cache_data(ttl=30)  # cache curto para atualizar rápido
def load_users():
    client, sheet, usuarios_ws, criterios_ws = init()
    df_users = pd.DataFrame(usuarios_ws.get_all_records())
    return df_users

df = load_users()

# Converter pontuação para número (Google retorna string)
df["pontuação"] = pd.to_numeric(df["pontuação"], errors="coerce").fillna(0).astype(int)

# Ordenar ranking
df = df.sort_values("pontuação", ascending=False)
df.columns = ["Username","Nome", "Senha","Pontuação"]

st.dataframe(df[["Nome", "Pontuação"]], hide_index=True)