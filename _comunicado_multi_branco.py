from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# 1) Expandir modos de geração
old_radio = '''        ["👤 Individual", "🏫 Por Turma(s)"],
        horizontal=True,
        key="modo_geracao_comunicado"
    )'''

new_radio = '''        [
            "👤 Individual",
            "👥 Vários alunos",
            "📝 Formulário em branco",
            "🏫 Por Turma(s)"
        ],
        horizontal=True,
        key="modo_geracao_comunicado"
    )'''

if old_radio not in texto:
    raise SystemExit("Nao achei o radio de modo de geracao")

texto = texto.replace(old_radio, new_radio, 1)

# 2) Inserir blocos Vários alunos + Formulário em branco ANTES do else Por Turmas
marcador = '''    # POR TURMAS
    # ======================================================

    else:

        st.subheader("🏫 Comunicado por Turmas")'''

if marcador not in texto:
    raise SystemExit("Nao achei o bloco POR TURMAS")

novos_modos = r'''
    # ======================================================
    # VÁRIOS ALUNOS
    # ======================================================

    elif modo == "👥 Vários alunos":

        st.markdown("### 👥 Seleção de vários estudantes")

        if df_alunos.empty:
            st.warning("⚠️ Cadastre alunos antes de gerar comunicados.")
            st.stop()

        turmas_filtro = sorted(
            df_alunos["turma"].dropna().astype(str).str.strip().unique().tolist()
        )
        turmas_filtro_sel = st.multiselect(
            "Filtrar por turma (opcional)",
            turmas_filtro,
            key="filtro_turma_varios_comunicado"
        )

        base_sel = df_alunos.copy()
        if turmas_filtro_sel:
            base_sel = base_sel[
                base_sel["turma"].astype(str).str.strip().isin(turmas_filtro_sel)
            ]

        opcoes_alunos = (
            base_sel.sort_values(["turma", "nome"])
            .apply(
                lambda r: f"{str(r.get('nome','')).strip()} | {str(r.get('turma','')).strip()} | RA {str(r.get('ra','')).strip()}",
                axis=1
            )
            .tolist()
        )

        alunos_sel = st.multiselect(
            "Selecione os estudantes",
            opcoes_alunos,
            key="alunos_varios_comunicado"
        )

        if not alunos_sel:
            st.info("ℹ️ Selecione ao menos um estudante.")
            st.stop()

        st.success(f"📊 {len(alunos_sel)} estudante(s) selecionado(s).")

        ocorrencia_data = {
            "data": data_comunicado.strftime("%d/%m/%Y") if data_comunicado else "",
            "categoria": "",
            "gravidade": "",
            "professor": "",
            "relato": "",
            "encaminhamento": "",
            "horario_chegada": "",
            "horario_permitido": "07:00",
            "justificativa": "",
        }

        if modelo_comunicado == "atraso":
            st.markdown("### Dados do atraso (comuns a todos)")
            c1, c2 = st.columns(2)
            with c1:
                horario_chegada_varios = st.text_input(
                    "Horário de chegada",
                    value="",
                    placeholder="Ex.: 07:18",
                    key="varios_horario_chegada"
                )
            with c2:
                horario_permitido_varios = st.text_input(
                    "Horário permitido",
                    value="07:00",
                    key="varios_horario_permitido"
                )
            justificativa_varios = st.text_area(
                "Justificativa apresentada",
                value="",
                height=80,
                key="varios_justificativa"
            )
            ocorrencia_data["horario_chegada"] = horario_chegada_varios.strip()
            ocorrencia_data["horario_permitido"] = (horario_permitido_varios.strip() or "07:00")
            ocorrencia_data["justificativa"] = justificativa_varios.strip()
            ocorrencia_data["categoria"] = "Chegar atrasado"

        medidas_aplicadas = []
        st.subheader("⚖️ Medidas")
        cols = st.columns(3)
        for i, medida in enumerate(medidas_opcoes):
            with cols[i % 3]:
                if st.checkbox(medida, key=f"medida_varios_{modelo_comunicado}_{medida}"):
                    medidas_aplicadas.append(medida)

        observacoes = st.text_area(
            "📝 Observações",
            height=80,
            key="observacoes_varios_comunicado"
        )

        if st.button(
            "📦 Gerar PDFs dos selecionados (ZIP)",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_varios"
        ):
            zip_buffer = BytesIO()
            total_gerados = 0
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for item in alunos_sel:
                    partes = [p.strip() for p in item.split("|")]
                    nome = partes[0] if len(partes) > 0 else ""
                    turma = partes[1] if len(partes) > 1 else ""
                    ra = partes[2].replace("RA", "").strip() if len(partes) > 2 else ""

                    aluno_data = {
                        "nome": nome,
                        "ra": ra,
                        "turma": turma,
                        "total_ocorrencias": 0,
                    }

                    pdf = gerar_pdf_comunicado(
                        aluno_data=aluno_data,
                        ocorrencia_data=ocorrencia_data,
                        medidas_aplicadas="\n".join(medidas_aplicadas),
                        observacoes=observacoes,
                        df_responsaveis=df_responsaveis,
                        modelo=modelo_comunicado,
                        data_comunicado=data_comunicado,
                    )

                    nome_seguro = "".join(
                        ch if ch.isalnum() or ch in ("_", "-") else "_"
                        for ch in nome.replace(" ", "_")
                    )
                    nome_pdf = f"Comunicado_{ra}_{nome_seguro}.pdf"
                    zip_file.writestr(nome_pdf, pdf.getvalue())
                    total_gerados += 1

            zip_buffer.seek(0)
            st.download_button(
                "📥 Baixar ZIP",
                data=zip_buffer.getvalue(),
                file_name=f"Comunicados_varios_{datetime.now().strftime('%Y%m%d_%H%M')}.zip",
                mime="application/zip",
                use_container_width=True,
                key="download_comunicados_varios"
            )
            st.success(f"✅ {total_gerados} comunicado(s) gerado(s).")

    # ======================================================
    # FORMULÁRIO EM BRANCO (PREENCHIMENTO MANUAL)
    # ======================================================

    elif modo == "📝 Formulário em branco":

        st.markdown("### 📝 Comunicado em branco")
        st.info(
            "Gera o PDF com Nome, RA e Turma em branco para preenchimento manual. "
            "Útil quando o estudante ainda não está na base."
        )

        ocorrencia_data = {
            "data": data_comunicado.strftime("%d/%m/%Y") if data_comunicado else "",
            "categoria": "Chegar atrasado" if modelo_comunicado == "atraso" else "",
            "gravidade": "",
            "professor": "",
            "relato": "",
            "encaminhamento": "",
            "horario_chegada": "",
            "horario_permitido": "07:00",
            "justificativa": "",
        }

        if modelo_comunicado == "atraso":
            st.markdown("### Dados do atraso (opcional)")
            c1, c2 = st.columns(2)
            with c1:
                h_cheg = st.text_input("Horário de chegada", key="branco_horario_chegada")
            with c2:
                h_perm = st.text_input("Horário permitido", value="07:00", key="branco_horario_permitido")
            just = st.text_area("Justificativa", height=70, key="branco_justificativa")
            ocorrencia_data["horario_chegada"] = h_cheg.strip()
            ocorrencia_data["horario_permitido"] = h_perm.strip() or "07:00"
            ocorrencia_data["justificativa"] = just.strip()

        medidas_aplicadas = []
        st.subheader("⚖️ Medidas")
        cols = st.columns(3)
        for i, medida in enumerate(medidas_opcoes):
            with cols[i % 3]:
                if st.checkbox(medida, key=f"medida_branco_{modelo_comunicado}_{medida}"):
                    medidas_aplicadas.append(medida)

        observacoes = st.text_area(
            "📝 Observações",
            height=80,
            key="observacoes_branco_comunicado"
        )

        if st.button(
            "📄 Gerar PDF em branco",
            type="primary",
            use_container_width=True,
            key="gerar_comunicado_branco"
        ):
            aluno_data = {
                "nome": "________________________________",
                "ra": "____________________",
                "turma": "____________________",
                "total_ocorrencias": 0,
            }
            pdf = gerar_pdf_comunicado(
                aluno_data=aluno_data,
                ocorrencia_data=ocorrencia_data,
                medidas_aplicadas="\n".join(medidas_aplicadas),
                observacoes=observacoes,
                df_responsaveis=df_responsaveis,
                modelo=modelo_comunicado,
                data_comunicado=data_comunicado,
            )
            st.download_button(
                "📥 Baixar PDF em branco",
                data=pdf.getvalue(),
                file_name=f"Comunicado_em_branco_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_comunicado_branco"
            )
            st.success("✅ PDF em branco gerado.")

    # POR TURMAS
    # ======================================================

    else:

        st.subheader("🏫 Comunicado por Turmas")'''

texto = texto.replace(marcador, novos_modos, 1)

path.write_text(texto, encoding="utf-8")
print("ok: modos Vários alunos + Formulário em branco inseridos")
