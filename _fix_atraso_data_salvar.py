from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")
original = texto

# 1) Inserir campo de DATA logo após a justificativa do atraso
marcador_just = '''            justificativa_comunicado = st.text_area(
                "Justificativa apresentada",
                value=str(
                    ocorrencia_data.get("justificativa", "")
                ).strip(),
                placeholder="Ex.: Transporte p?blico atrasado.",
                height=90,
                key="comunicado_justificativa_atraso"
            )'''

bloco_data = '''            justificativa_comunicado = st.text_area(
                "Justificativa apresentada",
                value=str(
                    ocorrencia_data.get("justificativa", "")
                ).strip(),
                placeholder="Ex.: Transporte público atrasado.",
                height=90,
                key="comunicado_justificativa_atraso"
            )

            data_atraso_comunicado = st.date_input(
                "Data do atraso",
                value=datetime.now().date(),
                format="DD/MM/YYYY",
                key="comunicado_data_atraso"
            )'''

if marcador_just not in texto:
    # tenta variação com acento correto no placeholder
    marcador_just2 = marcador_just.replace("p?blico", "público")
    if marcador_just2 in texto:
        texto = texto.replace(marcador_just2, bloco_data, 1)
    else:
        raise SystemExit("Nao achei o bloco da justificativa do atraso.")
else:
    texto = texto.replace(marcador_just, bloco_data, 1)

# 2) Depois de gravar campos do atraso em ocorrencia_data, inserir botão SALVAR
# Procuramos o trecho típico de atribuição dos campos de atraso
marcadores_pos = [
    'ocorrencia_data["atrasos_mes"] = (\n                atrasos_mes_comunicado\n            )',
    "ocorrencia_data['atrasos_mes'] = (\n                atrasos_mes_comunicado\n            )",
    'ocorrencia_data["atrasos_mes"] = atrasos_mes_comunicado',
]

inserido_salvar = False
bloco_salvar = '''

            ocorrencia_data["data"] = data_atraso_comunicado.strftime("%d/%m/%Y")

            if st.button(
                "💾 Salvar atraso",
                type="primary",
                use_container_width=True,
                key="salvar_atraso_comunicado"
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

bloco_salvar = bloco_salvar.replace("\\\\n", "\\n")

for m in marcadores_pos:
    if m in texto:
        texto = texto.replace(m, m + bloco_salvar, 1)
        inserido_salvar = True
        break

if not inserido_salvar:
    raise SystemExit("Nao achei o ponto para inserir o botao Salvar atraso.")

path.write_text(texto, encoding="utf-8")
print("ok: data do atraso + botao Salvar inseridos")
