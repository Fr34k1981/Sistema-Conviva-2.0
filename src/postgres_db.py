import os
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    db_url = None
    if "DATABASE_URL" in os.environ:
        db_url = os.environ["DATABASE_URL"]
    elif "postgres" in st.secrets and "url" in st.secrets["postgres"]:
        db_url = st.secrets["postgres"]["url"]
    elif "DATABASE_URL" in st.secrets:
        db_url = st.secrets["DATABASE_URL"]

    if not db_url:
        st.error("Configuração de banco de dados não encontrada.")
        st.stop()

    return psycopg2.connect(db_url, cursor_factory=RealDictCursor)
