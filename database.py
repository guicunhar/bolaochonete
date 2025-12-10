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
CRITERIOS_SHEET = "criterios"

def _open_sheets(service_account_file: str = "service_account.json"):
    creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME)

    usuarios = sheet.worksheet(USERS_SHEET)
    criterios = sheet.worksheet(CRITERIOS_SHEET)

    return client, sheet, usuarios, criterios

def init(service_account_file: str = "service_account.json"):
    with st.spinner("🔄 Aguarde"):
        return _open_sheets(service_account_file)


def create_user(username: str, name: str, password: str, service_account_file: str = "service_account.json"):
    client, sheet, usuarios, _ = init(service_account_file)

    # Verificar se usuário já existe
    records = usuarios.get_all_records()
    for r in records:
        if r.get("username") == username:
            return False, "Usuário já existe"

    # Criar hash da senha
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    linha = len(records) + 2  # +2 para considerar header e próxima linha
    usuarios.append_row(
        [username, name, password_hash, f'=SOMA(INDIRETO(A{linha} & "!I:I"))'],
        value_input_option="USER_ENTERED"
    )

    # Copiar MODELO
    modelo = sheet.worksheet("MODELO")
    new_sheet_info = modelo.copy_to(sheet.id)
    new_sheet = client.open_by_key(sheet.id).get_worksheet_by_id(new_sheet_info['sheetId'])
    new_sheet.update_title(username)

    return True, "Usuário criado com sucesso"

def validate_login(username: str, password: str, service_account_file: str = "service_account.json") -> Tuple[bool, str]:
    client, sheet, usuarios, _ = init(service_account_file)

    for r in usuarios.get_all_records():
        if r["username"] == username:
            stored_hash = r["password_hash"].encode()
            if bcrypt.checkpw(password.encode(), stored_hash):
                return True, r["name"]
            return False, "Senha incorreta"

    return False, "Usuário não encontrado"


def sidebar():
    st.sidebar.page_link('01_Tabela.py', label='Classificação')
    st.sidebar.page_link('pages/02_Login.py', label='Login')
    st.sidebar.page_link('pages/03_Meus_Palpites.py', label='Meus Palpites')