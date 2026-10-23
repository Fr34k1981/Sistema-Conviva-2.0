from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

if "Salvar atraso" in texto:
    raise SystemExit("Ja existe Salvar atraso. Nao inserir de novo.")

marcador = 'ocorrencia_data["data"] = data_atraso_comunicado.strftime("%d/%m/%Y")'
if marcador not in texto:
    # tenta aspas simples
    marcador = "ocorrencia_data['data'] = data_atraso_comunicado.strftime('%d/%m/%Y')"
if marcador not in texto:
    raise SystemExit("Nao achei ocorrencia_data[data] = data_atraso_comunicado")

bloco = '''ocorrencia_data["data"] = data_atraso_comunicado.strftime("%d/%m/%Y")

            if st.button(
                "💾 Salvar atraso",
                type="primary",
                use_container_width=True,
                key="salvar_atraso_comunicado_unico"
            ):
                data_reg = data_atraso_comunicado.strftime("%d/%m/%Y")
                horario_c = str(horario_chegada_comunicado).strip()
                horario_p = str(horario_permitido_comunicado).strip() or "07:00"
                just = str(justificativa_comunicado).strip() or "Não informada."
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
                    if verificar_ocorrencia_duplicada(ra_aluno, "Chegar atrasado", data_reg, df_base):
                        st.warning("Já existe ocorrência de atraso para este aluno nesta data.")
                    else:
                        if salvar_ocorrencia(nova_ocorrencia):
                            st.success("✅ Atraso salvo como ocorrência.")
                            carregar_ocorrencias.clear()
                            st.rerun()
                        else:
                            st.error("❌ Não foi possível salvar o atraso.")
                except Exception as e:
                    st.error(f"❌ Erro ao salvar atraso: {e}")
'''

bloco = bloco.replace("\\\\n", "\\n")
texto2 = texto.replace(marcador, bloco, 1)

print("Salvar atraso=", texto2.count("Salvar atraso"))
print("keys=", texto2.count("salvar_atraso_comunicado_unico"))
if texto2.count("Salvar atraso") != 1:
    raise SystemExit("Insercao falhou")

path.write_text(texto2, encoding="utf-8")
print("ok")
