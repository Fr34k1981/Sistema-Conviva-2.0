from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# 1) salvar_aluno: limpar os dois caches
old1 = '''    sucesso = _supabase_mutation("POST", "alunos", aluno, "salvar aluno")
    if sucesso:
        carregar_alunos.clear()
    return sucesso'''

new1 = '''    sucesso = _supabase_mutation("POST", "alunos", aluno, "salvar aluno")
    if sucesso:
        try:
            carregar_alunos.clear()
        except Exception:
            pass
        try:
            _supabase_get_dataframe.clear()
        except Exception:
            pass
    return sucesso'''

# 2) atualizar_aluno
old2 = '''    sucesso = _supabase_mutation("PATCH", f"alunos?ra=eq.{ra_url}", dados, "atualizar aluno")
    if sucesso:
        carregar_alunos.clear()
    return sucesso'''

new2 = '''    sucesso = _supabase_mutation("PATCH", f"alunos?ra=eq.{ra_url}", dados, "atualizar aluno")
    if sucesso:
        try:
            carregar_alunos.clear()
        except Exception:
            pass
        try:
            _supabase_get_dataframe.clear()
        except Exception:
            pass
    return sucesso'''

# 3) no fim da substituição, limpar de novo (garantia)
old3 = '''    try:
        carregar_alunos.clear()
    except Exception:
        pass

    df_atualizado = carregar_alunos()
    sync_stats = sincronizar_turmas_listas_com_base(df_atualizado, origem="substituicao_lista_oficial")'''

new3 = '''    try:
        carregar_alunos.clear()
    except Exception:
        pass
    try:
        _supabase_get_dataframe.clear()
    except Exception:
        pass

    df_atualizado = carregar_alunos()
    sync_stats = sincronizar_turmas_listas_com_base(df_atualizado, origem="substituicao_lista_oficial")'''

n = 0
for old, new in [(old1, new1), (old2, new2), (old3, new3)]:
    if old not in texto:
        raise SystemExit(f"Nao achei trecho para substituir:\n{old[:80]}")
    texto = texto.replace(old, new, 1)
    n += 1

path.write_text(texto, encoding="utf-8")
print(f"ok: {n} trechos de cache corrigidos")
