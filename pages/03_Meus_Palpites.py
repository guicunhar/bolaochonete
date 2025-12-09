import streamlit as st
from database import sidebar

sidebar()

RODADAS = {
    1: [("Brasil", "Argentina"), ("França", "Alemanha")],
    2: [("Portugal", "Espanha"), ("Inglaterra", "Itália")],
    3: [("Uruguai", "Holanda"), ("México", "Chile")],
}

# Verifica login
if not st.session_state.get("logged", False):
    st.warning("Você precisa fazer login para acessar esta página.")
else:
    st.title("Palpites – Bolão da Copa")
    st.markdown(f"<h4 style='text-align:center'>Bem-vindo, {st.session_state['name']}! Preencha seus palpites por rodada.</h4>", unsafe_allow_html=True)

    # Seleciona a rodada
    rodada = st.selectbox("Escolha a rodada", sorted(RODADAS.keys()))
    jogos = RODADAS[rodada]

    # Formulário de palpites
    with st.form(key=f"form_rodada_{rodada}"):
        palpites = {}
        for idx, (time1, time2) in enumerate(jogos):
            # Três colunas: Time1 | Inputs | Time2
            col1, col_inputs, col2 = st.columns([3,2,3])

            # Time1
            with col1:
                st.markdown(
                    f"<div style='display:flex; align-items:center; justify-content:center; height:95px;'><b>{time1}</b></div>",
                    unsafe_allow_html=True
                )

            # Inputs
            with col_inputs:
                input1_col, input2_col = st.columns([1,1])
                with input1_col:
                    palpites[f"{idx}_time1"] = st.number_input("", min_value=0, max_value=20, step=1, key=f"{rodada}_{idx}_t1")
                with input2_col:
                    palpites[f"{idx}_time2"] = st.number_input("", min_value=0, max_value=20, step=1, key=f"{rodada}_{idx}_t2")

            # Time2
            with col2:
                st.markdown(
                    f"<div style='display:flex; align-items:center; justify-content:center; height:95px;'><b>{time2}</b></div>",
                    unsafe_allow_html=True
                )

        enviar = st.form_submit_button("Enviar palpites")
        if enviar:
            st.success(f"Palpites da rodada {rodada} enviados com sucesso!")
            for idx, (time1, time2) in enumerate(jogos):
                t1 = palpites[f"{idx}_time1"]
                t2 = palpites[f"{idx}_time2"]
                st.markdown(
                    f"<div style='text-align:center'>{time1} {t1} x {t2} {time2}</div>",
                    unsafe_allow_html=True
                )
