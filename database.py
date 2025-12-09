import gspread
from google.oauth2.service_account import Credentials
import bcrypt
from typing import Tuple, List
import streamlit as st

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_NAME = "bolaochonete"
USERS_SHEET = "usuarios"
PALPITES_SHEET = "palpites"
RESULTADOS_SHEET = "resultados"
CRITERIOS_SHEET = "criterios"

def _open_sheets(service_account_file: str = "service_account.json"):
    creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME)
    usuarios = sheet.worksheet(USERS_SHEET)
    palpites = sheet.worksheet(PALPITES_SHEET)
    resultados = sheet.worksheet(RESULTADOS_SHEET)
    criterios = sheet.worksheet(CRITERIOS_SHEET)
    return usuarios, palpites, resultados, criterios


def ensure_headers(worksheet, headers: List[str]):
    current = worksheet.row_values(1)
    if current != headers:
        worksheet.update("A1", [headers])

def init(service_account_file: str = "service_account.json"):
    with st.spinner("🔄 Carregando dados"):
        usuarios, palpites, resultados, criterios= _open_sheets(service_account_file)
        ensure_headers(usuarios, ["username", "name","password_hash"])
        ensure_headers(palpites, ["username", "id_jogo", "palpite"])
        ensure_headers(resultados, ["id_jogo","fase", "resultado", "realA", "realB"])
        ensure_headers(criterios, ["fase","acerto_total","acerto_parcial"])
    return usuarios, palpites, resultados, criterios


def create_user(username: str, name: str, password: str, service_account_file: str = "service_account.json"):
    usuarios, _, _, _ = init(service_account_file)
    records = usuarios.get_all_records()

    for r in records:
        if r.get("username") == username:
            return False, "Usuário já existe"

    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    usuarios.append_row([username, name, password_hash])
    return True, "Usuário criado com sucesso"



def validate_login(username: str, password: str, service_account_file: str = "service_account.json") -> Tuple[bool, str]:
    usuarios, _, _ , _ = init(service_account_file)

    for r in usuarios.get_all_records():
        if r["username"] == username:
            stored_hash = r["password_hash"].encode()
            if bcrypt.checkpw(password.encode(), stored_hash):
                return True, r["name"]
            return False, "Senha incorreta"

    return False, "Usuário não encontrado"
