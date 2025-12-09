import streamlit as st
import pandas as pd
from database import init, sidebar

st.title("🏆 Classificação do Bolão")
st.write("Tabela baseada nos palpites enviados pelos usuários e nos resultados oficiais.")

sidebar()

# ---------------------------------------
# 🔥 Função CACHEADA para ler o Google Sheets
# ---------------------------------------
@st.cache_data(ttl=300)   # cache de 60 segundos (pode ajustar)
def load_data():
    usuarios_ws, palpites_ws, resultados_ws, criterios_ws = init()

    df_palpites = pd.DataFrame(palpites_ws.get_all_records())
    df_resultados = pd.DataFrame(resultados_ws.get_all_records())
    df_criterios = pd.DataFrame(criterios_ws.get_all_records())

    return df_palpites, df_resultados, df_criterios


# ---------------------------------------
# Carregar dados (META RÁPIDO AGORA)
# ---------------------------------------
df_palpites, df_resultados, df_criterios = load_data()

# ---------------------------------------
# Processamento
# ---------------------------------------
df_palpites["id_jogo"] = df_palpites["id_jogo"].astype(int)
df_resultados["id_jogo"] = df_resultados["id_jogo"].astype(int)

df = df_palpites.merge(df_resultados, on="id_jogo", how="left")
df = df.merge(df_criterios, on="fase", how="left")

df["pontos"] = 0

# Acertou vencedor
df.loc[df["palpite"] == df["resultado"], "pontos"] += df["acerto_parcial"]

# Acertou placar exato
df.loc[
    (df["timeA"].astype(int) == df["realA"].astype(int)) &
    (df["timeB"].astype(int) == df["realB"].astype(int)),
    "pontos"
] += df["acerto_total"]


# ---------------------------------------
# Ranking final
# ---------------------------------------
classificacao = (
    df.groupby("username")["pontos"]
    .sum()
    .reset_index()
    .sort_values("pontos", ascending=False)
)

st.subheader("📊 Classificação Atual do Bolão")
st.dataframe(classificacao, hide_index=True)
