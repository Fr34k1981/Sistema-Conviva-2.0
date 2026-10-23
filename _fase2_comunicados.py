from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

if "def salvar_comunicado(" in texto or "def carregar_comunicados(" in texto:
    raise SystemExit("Funcoes de comunicado ja existem. Abortado.")

marcador = "def salvar_ocorrencia(ocorrencia: dict) -> bool:"
if marcador not in texto:
    raise SystemExit("Nao achei salvar_ocorrencia para ancorar a insercao.")

funcoes = '''
@com_tratamento_erro
def carregar_comunicados() -> pd.DataFrame:
    """Carrega registros da tabela comunicados."""
    try:
        df = _supabase_get_dataframe(
            "comunicados?select=*&order=data_comunicado.desc,id.desc",
            "carregar comunicados"
        )
        if df is None or df.empty:
            return pd.DataFrame()
        return df
    except Exception:
        return pd.DataFrame()


@com_tratamento_erro
def salvar_comunicado(dados: dict) -> bool:
    """Salva um comunicado institucional na tabela comunicados."""
    valido, msg = Validadores.validar_nao_vazio(dados.get("nome_aluno"), "Nome do aluno")
    if not valido:
        raise ErroValidacao("nome_aluno", msg)
    if not dados.get("data_comunicado"):
        raise ErroValidacao("data_comunicado", "Data do comunicado e obrigatoria")
    sucesso = _supabase_mutation(
        "POST",
        "comunicados",
        dados,
        "salvar comunicado"
    )
    if sucesso:
        try:
            carregar_comunicados.clear()
        except Exception:
            pass
    return sucesso


'''

# Insere ANTES de salvar_ocorrencia
texto2 = texto.replace(marcador, funcoes + marcador, 1)

print("carregar_comunicados=", texto2.count("def carregar_comunicados("))
print("salvar_comunicado=", texto2.count("def salvar_comunicado("))
if texto2.count("def carregar_comunicados(") != 1 or texto2.count("def salvar_comunicado(") != 1:
    raise SystemExit("Insercao falhou")

path.write_text(texto2, encoding="utf-8")
print("ok: FASE 2 funcoes inseridas")
