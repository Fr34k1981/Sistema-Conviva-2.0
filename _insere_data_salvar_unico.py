from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

if "data_atraso_comunicado = st.date_input" in texto or "Salvar atraso" in texto:
    raise SystemExit("Ja existe data ou Salvar. Abortado para nao duplicar.")

marcador = 'key="comunicado_justificativa_atraso"\n            )'
if marcador not in texto:
    raise SystemExit("Nao achei justificativa_atraso")

bloco = (
    'key="comunicado_justificativa_atraso"\n'
    "            )\n\n"
    "            data_atraso_comunicado = st.date_input(\n"
    '                "Data do atraso",\n'
    "                value=datetime.now().date(),\n"
    '                format="DD/MM/YYYY",\n'
    '                key="comunicado_data_atraso_unica"\n'
    "            )\n\n"
    "            if st.button(\n"
    '                "💾 Salvar atraso",\n'
    '                type="primary",\n'
    "                use_container_width=True,\n"
    '                key="salvar_atraso_comunicado_unico"\n'
    "            ):\n"
    '                data_reg = data_atraso_comunicado.strftime("%d/%m/%Y")\n'
    "                horario_c = str(horario_chegada_comunicado).strip()\n"
    '                horario_p = str(horario_permitido_comunicado).strip() or "07:00"\n'
    '                just = str(justificativa_comunicado).strip() or "Não informada."\n'
    "                relato_atraso = (\n"
    '                    f"Atraso na entrada da escola. "\n'
    '                    f"Horário permitido: {horario_p}. "\n'
    '                    f"Horário de chegada: {horario_c or \'Não informado\'}. "\n'
    '                    f"Justificativa: {just}."\n'
    "                )\n"
    "                nova_ocorrencia = {\n"
    '                    "data": data_reg,\n'
    '                    "aluno": nome_aluno,\n'
    '                    "ra": ra_aluno,\n'
    '                    "turma": turma_aluno,\n'
    '                    "categoria": "Chegar atrasado",\n'
    '                    "gravidade": "Leve",\n'
    '                    "relato": relato_atraso,\n'
    '                    "encaminhamento": (\n'
    '                        "Registrar em ata\\n"\n'
    '                        "Conversar com o aluno\\n"\n'
    '                        "Notificar famílias (se recorrente)\\n"\n'
    '                        "Verificar motivo dos atrasos\\n"\n'
    '                        "Orientação Educacional"\n'
    "                    ),\n"
    '                    "professor": str(ocorrencia_data.get("professor", "")).strip() or "Equipe escolar",\n'
    "                }\n"
    "                try:\n"
    '                    df_base = df_ocorrencias if "df_ocorrencias" in dir() else pd.DataFrame()\n'
    '                    if verificar_ocorrencia_duplicada(ra_aluno, "Chegar atrasado", data_reg, df_base):\n'
    '                        st.warning("Já existe ocorrência de atraso para este aluno nesta data.")\n'
    "                    else:\n"
    "                        if salvar_ocorrencia(nova_ocorrencia):\n"
    '                            st.success("✅ Atraso salvo como ocorrência.")\n'
    "                            carregar_ocorrencias.clear()\n"
    "                            st.rerun()\n"
    "                        else:\n"
    '                            st.error("❌ Não foi possível salvar o atraso.")\n'
    "                except Exception as e:\n"
    '                    st.error(f"❌ Erro ao salvar atraso: {e}")\n'
)

bloco = bloco.replace("\\\\n", "\\n")
texto2 = texto.replace(marcador, bloco, 1)

print("date_input=", texto2.count("data_atraso_comunicado = st.date_input"))
print("Salvar atraso=", texto2.count("Salvar atraso"))
print("keys=", texto2.count("salvar_atraso_comunicado_unico"))

if texto2.count("data_atraso_comunicado = st.date_input") != 1:
    raise SystemExit("Data nao ficou 1")
if texto2.count("Salvar atraso") != 1:
    raise SystemExit("Salvar nao ficou 1")

path.write_text(texto2, encoding="utf-8")
print("ok")
