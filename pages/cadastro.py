import streamlit as st
import gspread
from database import create_user, sidebar

sidebar()

st.set_page_config(page_title="Cadastro - Bolão da Copa")

st.title("Cadastro – Bolão da Copa 📝")

if "logged" in st.session_state and st.session_state["logged"]:
    st.info("Você já está logado.")
    st.stop()

st.subheader("Crie sua conta abaixo")

with st.form("form_cadastro"):
    username = st.text_input("Username").strip().lower()
    name = st.text_input("Nome").strip()
    password = st.text_input("Senha", type="password")
    password2 = st.text_input("Confirmar senha", type="password")

    submit = st.form_submit_button("Cadastrar")

if submit:
    if not username or not name or not password:
        st.error("Preencha todos os campos.")
        st.stop()

    if " " in username:
        st.error("O usuário não pode conter espaços.")
        st.stop()

    if password != password2:
        st.error("As senhas não coincidem.")
        st.stop()

    ok, msg = create_user(username, name, password)

    if "logged" not in st.session_state:
        st.session_state["logged"] = False

    if ok:
        st.success(msg)
    else:
        st.error(msg)
