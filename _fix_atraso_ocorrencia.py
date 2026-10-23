from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

alvo = '''        if st.button(
            "📄 Gerar Comunicado (PDF)",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_individual"
        ):

            aluno_data = {
                "nome": nome_aluno,
                "ra": ra_aluno,
                "turma": turma_aluno,
                "total_ocorrencias": len(ocorrencias_aluno)
            }

            pdf_buffer = gerar_pdf_comunicado(
                aluno_data=aluno_data,
                ocorrencia_data=ocorrencia_data,
                medidas_aplicadas="\\n".join(medidas_aplicadas),
                observacoes=observacoes,
                df_responsaveis=df_responsaveis,
                modelo=modelo_comunicado
            )'''

novo = '''        if st.button(
            "📄 Gerar Comunicado (PDF)",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_individual"
        ):

            # Opção A: atraso sempre grava ocorrência automaticamente
            if str(modelo_comunicado).lower() == "atraso":
                data_reg = datetime.now().strftime("%d/%m/%Y %H:%M")
                horario_c = str(ocorrencia_data.get("horario_chegada", "")).strip()
                horario_p = str(ocorrencia_data.get("horario_permitido", "07:00")).strip() or "07:00"
                just = str(ocorrencia_data.get("justificativa", "")).strip() or "Não informada."
                relato_atraso = (
                    f"Atraso na entrada da escola. "
                    f"Horário permitido: {horario_p}. "
                    f"Horário de chegada: {horario_c or 'Não informado'}. "
                    f"Justificativa: {just}."
                )
                nova_ocorrencia = {
                    "data": data_reg,
                    "aluno": nome_aluno,
                    "ra": ra_aluno,
                    "turma": turma_aluno,
                    "categoria": "Chegar atrasado",
                    "gravidade": "Leve",
                    "relato": relato_atraso,
                    "encaminhamento": (
                        "Registrar em ata\\n"
                        "Conversar com o aluno\\n"
                        "Notificar famílias (se recorrente)\\n"
                        "Verificar motivo dos atrasos\\n"
                        "Orientação Educacional"
                    ),
                    "professor": str(ocorrencia_data.get("professor", "")).strip() or "Equipe escolar",
                }
                try:
                    df_base = df_ocorrencias if "df_ocorrencias" in dir() else pd.DataFrame()
                    if not verificar_ocorrencia_duplicada(ra_aluno, "Chegar atrasado", data_reg, df_base):
                        if salvar_ocorrencia(nova_ocorrencia):
                            st.success("✅ Ocorrência de atraso registrada automaticamente.")
                            carregar_ocorrencias.clear()
                    ocorrencia_data["categoria"] = "Chegar atrasado"
                    ocorrencia_data["data"] = data_reg
                    ocorrencia_data["relato"] = relato_atraso
                except Exception as e:
                    st.warning(f"PDF será gerado, mas falhou o registro da ocorrência: {e}")

            total_ocorrencias_pdf = len(ocorrencias_aluno)
            if str(modelo_comunicado).lower() == "atraso":
                total_ocorrencias_pdf = len(ocorrencias_aluno) + 1

            aluno_data = {
                "nome": nome_aluno,
                "ra": ra_aluno,
                "turma": turma_aluno,
                "total_ocorrencias": total_ocorrencias_pdf
            }

            pdf_buffer = gerar_pdf_comunicado(
                aluno_data=aluno_data,
                ocorrencia_data=ocorrencia_data,
                medidas_aplicadas="\\n".join(medidas_aplicadas),
                observacoes=observacoes,
                df_responsaveis=df_responsaveis,
                modelo=modelo_comunicado
            )'''

# O arquivo real usa quebras reais, não \\n escapado no join
alvo = alvo.replace("\\\\n", "\\n")
novo = novo.replace("\\\\n", "\\n")

if alvo not in texto:
    raise SystemExit("Nao achei o bloco exato do botao Gerar Comunicado. Pare e me avise.")

texto2 = texto.replace(alvo, novo, 1)
path.write_text(texto2, encoding="utf-8")
print("ok: atraso agora grava ocorrencia automaticamente")
