import streamlit as st
from database import validate_login, sidebar

sidebar()

if "logged" not in st.session_state:
    st.session_state["logged"] = False

st.title("Login – Bolão da Copa")

if st.session_state["logged"] == False:
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        ok, msg = validate_login(username, password)
        if ok:
            st.session_state["logged"] = True
            st.session_state["username"] = username
            st.session_state["name"] = msg
            st.success(f"Bem-vindo, {msg}!")
        
        else:
            st.error(msg)
else:
    st.info(f"{st.session_state['name']}, você já está logado.")