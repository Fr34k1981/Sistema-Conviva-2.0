"""Autenticacao OIDC e autorizacao por perfil para o Sistema Conviva."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import streamlit as st


@dataclass(frozen=True)
class AccessContext:
    role: str
    email: str = ""
    student_ra: str = ""
    teacher_name: str = ""


_SYNC_DELETE_TABLES = {
    "perfil_tutorado",
    "rendimento_bimestral",
    "tutoria_individual",
    "tutoria_coletiva",
}


def classify_email(
    email: str,
    staff_emails: list[str] | tuple[str, ...],
    portal_accounts: dict[str, str],
    manager_emails: list[str] | tuple[str, ...] = (),
    teacher_accounts: dict[str, str] | None = None,
) -> AccessContext:
    """Classifica a conta por listas explicitas, priorizando o perfil da equipe."""
    normalized_email = str(email or "").strip().casefold()
    if not normalized_email:
        return AccessContext("unauthorized")

    normalized_managers = {str(value).strip().casefold() for value in manager_emails}
    if normalized_email in normalized_managers:
        return AccessContext("manager", normalized_email)

    normalized_staff = {str(value).strip().casefold() for value in staff_emails}
    if normalized_email in normalized_staff:
        teacher_name = ""
        for account_email, name in (teacher_accounts or {}).items():
            if str(account_email).strip().casefold() == normalized_email:
                teacher_name = str(name or "").strip()
                break
        return AccessContext("staff", normalized_email, teacher_name=teacher_name)

    for account_email, student_ra in portal_accounts.items():
        if str(account_email).strip().casefold() == normalized_email:
            ra = str(student_ra or "").strip()
            if ra:
                return AccessContext("parent", normalized_email, ra)

    return AccessContext("unauthorized", normalized_email)


def can_delete(
    role: str,
    table: str,
    where_columns: list[str],
    where_values: list[Any],
    teacher_name: str = "",
    allow_sync: bool = False,
) -> bool:
    """Enforce manager-only deletion except owner-scoped tutoring and internal sync."""
    if role in {"manager", "local"}:
        return True
    if allow_sync and table in _SYNC_DELETE_TABLES:
        return True
    if role != "staff" or table != "tutoria" or not teacher_name:
        return False

    predicates = {
        (column, str(value).strip().casefold())
        for column, value in zip(where_columns, where_values)
    }
    return ("professora", teacher_name.strip().casefold()) in predicates


def _secret(name: str, default: Any = None) -> Any:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def _is_production() -> bool:
    if Path(__file__).resolve().as_posix().startswith("/mount/src/"):
        return True

    configured = os.getenv("APP_ENV") or _secret("APP_ENV")
    if configured:
        return str(configured).strip().casefold() not in {"dev", "development", "local", "test"}

    return False


def require_access(required_role: str | None = None) -> AccessContext:
    """Require OIDC and an allowlisted role in production; permit trusted local development."""
    if not _is_production():
        return AccessContext("local")

    try:
        user = st.user
        logged_in = bool(user.is_logged_in)
    except Exception:
        st.error("A autenticacao OIDC nao esta disponivel. Verifique a configuracao do Streamlit.")
        st.stop()

    if not logged_in:
        st.info("Entre com uma conta autorizada para acessar o Sistema Conviva.")
        if st.button("Entrar", type="primary"):
            st.login()
        st.stop()

    staff_emails = _secret("APP_ALLOWED_EMAILS", [])
    if isinstance(staff_emails, str):
        staff_emails = [value.strip() for value in staff_emails.split(",") if value.strip()]
    manager_emails = _secret("APP_MANAGER_EMAILS", [])
    if isinstance(manager_emails, str):
        manager_emails = [value.strip() for value in manager_emails.split(",") if value.strip()]
    portal_accounts = _secret("APP_PORTAL_RA_BY_EMAIL", {})
    if not isinstance(portal_accounts, dict):
        portal_accounts = {}
    teacher_accounts = _secret("APP_TEACHER_BY_EMAIL", {})
    if not isinstance(teacher_accounts, dict):
        teacher_accounts = {}

    context = classify_email(
        user.email,
        staff_emails or [],
        portal_accounts,
        manager_emails or [],
        teacher_accounts,
    )
    if context.role == "unauthorized":
        st.error("Esta conta nao esta autorizada para acessar o sistema.")
        if st.button("Sair"):
            st.logout()
        st.stop()

    role_allowed = context.role == required_role or (
        required_role == "staff" and context.role == "manager"
    )
    if required_role and not role_allowed:
        st.error("Esta area nao esta disponivel para o perfil da sua conta.")
        st.stop()

    return context