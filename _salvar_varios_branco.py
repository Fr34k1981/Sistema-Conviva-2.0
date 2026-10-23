from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# 1) No modo Vários: botão Salvar antes do Gerar ZIP
marcador_varios = '''        if st.button(
            "📦 Gerar PDFs dos selecionados (ZIP)",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_varios"
        ):'''

bloco_salvar_varios = '''        if st.button(
            "💾 Salvar comunicados selecionados",
            type="secondary",
            use_container_width=True,
            key="salvar_comunicado_varios"
        ):
            salvos = 0
            falhas = 0
            for item in alunos_sel:
                partes = [p.strip() for p in item.split("|")]
                nome = partes[0] if len(partes) > 0 else ""
                turma = partes[1] if len(partes) > 1 else ""
                ra = partes[2].replace("RA", "").strip() if len(partes) > 2 else ""
                dados_comunicado = {
                    "data_comunicado": (
                        data_comunicado.strftime("%Y-%m-%d")
                        if hasattr(data_comunicado, "strftime")
                        else str(data_comunicado)
                    ),
                    "ra_aluno": ra,
                    "nome_aluno": nome,
                    "turma": turma,
                    "tipo_comunicado": str(modelo_comunicado).strip() or "geral",
                    "modelo": str(modelo_comunicado).strip() or "geral",
                    "horario_permitido": str(ocorrencia_data.get("horario_permitido", "")).strip(),
                    "horario_chegada": str(ocorrencia_data.get("horario_chegada", "")).strip(),
                    "justificativa": str(ocorrencia_data.get("justificativa", "")).strip(),
                    "medidas_aplicadas": "\\n".join(medidas_aplicadas),
                    "observacoes": str(observacoes).strip(),
                    "professor_responsavel": "Equipe escolar",
                    "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                try:
                    if salvar_comunicado(dados_comunicado):
                        salvos += 1
                    else:
                        falhas += 1
                except Exception:
                    falhas += 1
            if salvos:
                st.success(f"✅ {salvos} comunicado(s) salvo(s) no banco.")
                try:
                    carregar_comunicados.clear()
                except Exception:
                    pass
            if falhas:
                st.error(f"❌ {falhas} falha(s) ao salvar.")

        if st.button(
            "📦 Gerar PDFs dos selecionados (ZIP)",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_varios"
        ):'''

bloco_salvar_varios = bloco_salvar_varios.replace("\\\\n", "\\n")

if marcador_varios not in texto:
    raise SystemExit("Nao achei botao Gerar ZIP varios")
if "salvar_comunicado_varios" in texto:
    print("salvar varios ja existe")
else:
    texto = texto.replace(marcador_varios, bloco_salvar_varios, 1)
    print("ok: salvar varios inserido")

# 2) No modo branco: botão Salvar antes do Gerar PDF
marcador_branco = '''        if st.button(
            "📄 Gerar PDF em branco",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_branco"
        ):'''

bloco_salvar_branco = '''        if st.button(
            "💾 Salvar registro em branco",
            type="secondary",
            use_container_width=True,
            key="salvar_comunicado_branco"
        ):
            dados_comunicado = {
                "data_comunicado": (
                    data_comunicado.strftime("%Y-%m-%d")
                    if hasattr(data_comunicado, "strftime")
                    else str(data_comunicado)
                ),
                "ra_aluno": "",
                "nome_aluno": "A PREENCHER",
                "turma": "",
                "tipo_comunicado": str(modelo_comunicado).strip() or "geral",
                "modelo": str(modelo_comunicado).strip() or "geral",
                "horario_permitido": str(ocorrencia_data.get("horario_permitido", "")).strip(),
                "horario_chegada": str(ocorrencia_data.get("horario_chegada", "")).strip(),
                "justificativa": str(ocorrencia_data.get("justificativa", "")).strip(),
                "medidas_aplicadas": "\\n".join(medidas_aplicadas),
                "observacoes": str(observacoes).strip(),
                "professor_responsavel": "Equipe escolar",
                "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            try:
                if salvar_comunicado(dados_comunicado):
                    st.success("✅ Registro em branco salvo no banco.")
                    try:
                        carregar_comunicados.clear()
                    except Exception:
                        pass
                else:
                    st.error("❌ Nao foi possivel salvar.")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")

        if st.button(
            "📄 Gerar PDF em branco",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_branco"
        ):'''

bloco_salvar_branco = bloco_salvar_branco.replace("\\\\n", "\\n")

if marcador_branco not in texto:
    raise SystemExit("Nao achei botao Gerar PDF branco")
if "salvar_comunicado_branco" in texto:
    print("salvar branco ja existe")
else:
    texto = texto.replace(marcador_branco, bloco_salvar_branco, 1)
    print("ok: salvar branco inserido")

path.write_text(texto, encoding="utf-8")
print("fim")
