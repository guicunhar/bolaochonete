import streamlit as st
from database import validate_login 

st.title("Login – Bolão da Copa")

username = st.text_input("Usuário")
password = st.text_input("Senha", type="password")

if st.button("Entrar"):
    ok, msg = validate_login(username, password)
    if ok:
        st.session_state["logged"] = True
        st.session_state["username"] = username
        st.session_state["name"] = msg
        st.success(f"Bem-vindo, {msg}!")
        st.switch_page("pages/palpites.py")
    else:
        st.error(msg)
