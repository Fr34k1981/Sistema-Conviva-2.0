from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

inicio = texto.find("    # ======================================================\n    # ======================================================\n    # COMUNICADOS SALVOS - HISTORICO")
if inicio == -1:
    inicio = texto.find("    # COMUNICADOS SALVOS - HISTORICO")
if inicio == -1:
    raise SystemExit("Nao achei HISTORICO de comunicados")

# fim do bloco historico: logo antes de VÁRIOS ALUNOS
fim = texto.find("    # ======================================================\n    # VÁRIOS ALUNOS", inicio)
if fim == -1:
    fim = texto.find('    elif modo == "👥 Vários alunos":', inicio)
if fim == -1:
    raise SystemExit("Nao achei VÁRIOS ALUNOS")

bloco_historico = texto[inicio:fim]

# remove historico do meio
texto2 = texto[:inicio] + texto[fim:]

# troca elif invalidos: garantir que Vários vem logo apos Individual
# Achar fim do Por Turmas (download lote / success) para colocar historico no final
marcador_fim_lote = '            st.success(\n                f"✅ {total_gerados} comunicado(s) gerado(s) "\n                f"com o modelo \'{modelo_nome}\'."\n            )'

idx = texto2.find(marcador_fim_lote)
if idx == -1:
    # tenta sem escape
    marcador_fim_lote = 'f"✅ {total_gerados} comunicado(s) gerado(s) "'
    idx = texto2.find(marcador_fim_lote)
    if idx == -1:
        raise SystemExit("Nao achei fim do lote por turmas")
    # avancar ate fim da linha do success
    idx = texto2.find("\n", texto2.find("st.success", idx))
    # achar o fechamento aproximado
    # procurar o ultimo st.success do lote
    pos = 0
    last = -1
    while True:
        p = texto2.find('total_gerados} comunicado(s) gerado(s)', pos)
        if p == -1:
            break
        last = p
        pos = p + 1
    if last == -1:
        raise SystemExit("Nao achei success final do lote")
    # fim da linha apos esse success
    fim_bloco = texto2.find("\n", texto2.find(")", last))
    insert_at = fim_bloco + 1
else:
    insert_at = idx + len(marcador_fim_lote)

texto3 = texto2[:insert_at] + "\n\n" + bloco_historico + texto2[insert_at:]

path.write_text(texto3, encoding="utf-8")
print("ok: historico movido para depois dos modos")
