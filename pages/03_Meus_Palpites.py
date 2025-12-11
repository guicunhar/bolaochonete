import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from database import sidebar
from datetime import datetime

sidebar()

# --- Autenticação Google ---
SHEET_NAME = "bolaochonete"
credentials = Credentials.from_service_account_file(
    "service_account.json",
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
)
gc = gspread.authorize(credentials)
sh = gc.open(SHEET_NAME)

# --- Carregar dados ---
def load_sheet():
    values = worksheet.get_all_values()
    headers = values[0]
    fixed_headers = [h if h.strip() != "" else f"col_{i}" for i, h in enumerate(headers)]
    return pd.DataFrame(values[1:], columns=fixed_headers)

if st.session_state["logged"] == False:
    st.warning("⚠️ Você precisa estar logado para acessar esta página.")
else:
    worksheet = sh.worksheet(st.session_state['username'])
    # Inicializa session_state apenas se ainda não existir
    if "df_edit" not in st.session_state:
        st.session_state.df_edit = load_sheet()

    df = st.session_state.df_edit
    formula_col = "Pontos"

    # --- Determina quais índices NÃO devem ser editados ---
    blocked_indices = []
    for idx, row in df.iterrows():
        data_str = row['Dia']
        hora_str = row['Hora']

        # Normaliza hora
        if "h" in hora_str:
            hora_str = hora_str.replace("h", ":")
            if len(hora_str.split(":")[1]) == 0:
                hora_str += "00"

        datetime_str = f"{data_str} {hora_str}"
        try:
            jogo_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")
            if jogo_datetime <= datetime.now():
                blocked_indices.append(idx)
        except:
            pass

    # --- Editor ---
    # Criamos uma cópia do DF e transformamos em string para "desabilitar" linhas passadas
    df_editor = df.copy()
    for idx in blocked_indices:
        df_editor.loc[idx, "Gols A"] = df.loc[idx, "Gols A"]
        df_editor.loc[idx, "Gols B"] = df.loc[idx, "Gols B"]

    edited_df = st.data_editor(
        df_editor,
        key="editor_sheet",
        disabled=["Fase", "Dia", "Hora", "x", "Time A", "Time B", "Pontos"],
        hide_index=True,
        column_config={
            "Gols A": st.column_config.NumberColumn("Gols A", format="%d"),
            "Gols B": st.column_config.NumberColumn("Gols B", format="%d"),
        }
    )

    # Botão para salvar alterações
    if st.button("💾 Salvar alterações"):
        df_to_update = edited_df.drop(columns=[formula_col])

        # Ignora alterações nas linhas bloqueadas
        for idx in blocked_indices:
            df_to_update.loc[idx, "Gols A"] = df.loc[idx, "Gols A"]
            df_to_update.loc[idx, "Gols B"] = df.loc[idx, "Gols B"]

        worksheet.update(
            [df_to_update.columns.values.tolist()] + df_to_update.values.tolist(),
            value_input_option="USER_ENTERED"
        )

        # Atualiza a planilha com pontuação
        st.session_state.df_edit = load_sheet()
