from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Localiza o bloco inteiro da grade (do markdown --- ate antes de Cadastrar Assinaturas)
inicio = texto.find('    # --------------------------------------------------\n    # GRADE DE HORÁRIOS (Turno 1)')
if inicio == -1:
    inicio = texto.find("📅 Grade de horários do professor")
    if inicio != -1:
        # voltar ate o st.markdown("---") anterior
        inicio = texto.rfind("st.markdown(\"---\")", 0, inicio)
        if inicio == -1:
            raise SystemExit("Nao achei inicio grade")
        # incluir a linha do markdown
        inicio = texto.rfind("\n", 0, inicio) + 1

fim = texto.find("# PÁGINA 👤 CADASTRAR ASSINATURAS", inicio)
if fim == -1:
    raise SystemExit("Nao achei fim grade / Assinaturas")

# volta para o inicio do comentario da pagina assinaturas
fim_bloco = texto.rfind("    # ======================================================", inicio, fim)
if fim_bloco == -1:
    fim_bloco = fim

novo = r'''
    # --------------------------------------------------
    # ABAS: Cadastro | Grade de horarios
    # --------------------------------------------------
    aba_cad_prof, aba_grade_prof = st.tabs([
        "👥 Cadastro de professores",
        "📅 Grade de horários (Turno 1)"
    ])

    with aba_grade_prof:
        st.subheader("📅 Grade de horários · Turno 1")
        st.caption("Quadro completo de aulas · consulta por professor ou grade cheia")

        try:
            carregar_grade_horaria.clear()
        except Exception:
            pass

        try:
            df_grade = carregar_grade_horaria("Turno 1", 2026)
        except Exception:
            df_grade = pd.DataFrame()

        if df_grade is None or df_grade.empty:
            st.warning("⚠️ Grade ainda não importada.")
        else:
            def _norm_txt(v):
                return normalizar_texto(str(v or ""))

            def _norm_turma_key(t):
                s = str(t or "").upper()
                s = s.replace("º", "").replace("°", "").replace(" ", "")
                s = s.replace("ANO", "")
                s = s.replace("-", "")
                return s

            mapa_turma_cols = [
                ("6A", "6ºA"),
                ("6B", "6ºB"),
                ("7A", "7ºA"),
                ("7C", "7ºC"),
                ("8A", "8ºA"),
                ("8B", "8ºB"),
                ("8C", "8ºC"),
                ("9A", "9ºA"),
                ("9B", "9ºB"),
                ("9C", "9ºC"),
                ("3ATEC", "3ºA-TEC"),
                ("3BTEC", "3ºB-TEC"),
            ]

            professores_grade = sorted({
                str(p).strip() for p in df_grade["professor"].dropna().astype(str) if str(p).strip()
            })

            modo_grade = st.radio(
                "Visualização",
                ["Grade completa (todas as turmas)", "Filtrar por professor"],
                horizontal=True,
                key="modo_grade_horaria",
            )

            dia_filtro = st.selectbox(
                "Dia",
                ["Todos", "Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
                key="grade_horaria_dia_sel",
            )

            prof_grade_sel = None
            if modo_grade == "Filtrar por professor":
                prof_grade_sel = st.selectbox(
                    "Professor(a)",
                    professores_grade,
                    key="grade_horaria_prof_sel",
                )

            df_base = df_grade.copy()
            if dia_filtro != "Todos":
                df_base = df_base[
                    df_base["dia_semana"].astype(str).str.strip().str.lower()
                    == dia_filtro.strip().lower()
                ]

            if modo_grade == "Filtrar por professor" and prof_grade_sel:
                pn = _norm_txt(prof_grade_sel)
                df_lista = df_base[
                    df_base["professor"].astype(str).map(_norm_txt).map(
                        lambda p: pn in p or p in pn
                    )
                ].copy()
                if df_lista.empty:
                    st.info(f"Nenhuma aula para **{prof_grade_sel}**.")
                else:
                    ordem_dias = {"Segunda": 1, "Terça": 2, "Terca": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5}
                    df_lista["_ord"] = df_lista["dia_semana"].map(lambda d: ordem_dias.get(str(d), 99))
                    df_lista = df_lista.sort_values(["_ord", "aula", "turma"])
                    st.success(f"**{len(df_lista)}** aula(s) de **{prof_grade_sel}**")
                    st.dataframe(
                        df_lista[["dia_semana", "aula", "turma", "disciplina", "professor"]].rename(
                            columns={
                                "dia_semana": "Dia",
                                "aula": "Aula",
                                "turma": "Turma",
                                "disciplina": "Disciplina",
                                "professor": "Professor",
                            }
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )

            # Grade completa sempre disponivel (ou so no modo completa)
            if modo_grade == "Grade completa (todas as turmas)":
                st.markdown("### 🗓️ Grade completa")
                df_full = df_base.copy()
                df_full["_tk"] = df_full["turma"].map(_norm_turma_key)
                prof_n = _norm_txt(prof_grade_sel) if prof_grade_sel else ""

                dias_show = (
                    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
                    if dia_filtro == "Todos"
                    else [dia_filtro]
                )

                for dia in dias_show:
                    df_dia = df_full[
                        df_full["dia_semana"].astype(str).str.strip().str.lower() == dia.lower()
                    ]
                    if df_dia.empty:
                        continue
                    st.markdown(f"**{dia.upper()}**")
                    linhas = []
                    for aula in range(1, 8):
                        row = {"Aula": aula}
                        df_aula = df_dia[pd.to_numeric(df_dia["aula"], errors="coerce") == aula]
                        for key, label in mapa_turma_cols:
                            cel = df_aula[df_aula["_tk"] == key]
                            if cel.empty:
                                row[label] = ""
                            else:
                                r0 = cel.iloc[0]
                                txt = f"{r0['disciplina']} - {r0['professor']}"
                                if prof_n and (
                                    prof_n in _norm_txt(r0["professor"])
                                    or _norm_txt(r0["professor"]) in prof_n
                                ):
                                    txt = f"★ {txt}"
                                row[label] = txt
                        linhas.append(row)
                    st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)

    with aba_cad_prof:
        st.caption("Cadastro e lista de professores")
'''

# O problema: o cadastro atual esta FORA de qualquer aba.
# Estrategia: envolver o conteudo existente de cadastro NA aba_cad_prof
# e colocar a grade na aba_grade_prof.
# Mais seguro: inserir tabs no INICIO da pagina e indentar e complexo.
# Alternativa pratica: colocar a grade numa aba e deixar o cadastro como esta
# logo abaixo da aba (streamlit tabs so isolam o with block).

# Substituir so o bloco da grade antiga pelo novo (abas so na grade + aviso)
# E no inicio da pagina Cadastrar Professores NAO mexer no form.

texto2 = texto[:inicio] + novo + texto[fim_bloco:]
path.write_text(texto2, encoding="utf-8")
print("ok: aba grade + normalizacao de turmas")
