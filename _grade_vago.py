from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# 1) Garantir 3 abas na definicao
old_tabs = '''    aba_cad_prof, aba_grade_prof = st.tabs([
        "👥 Cadastro de professores",
        "📅 Grade de horários (Turno 1)"
    ])'''

new_tabs = '''    aba_cad_prof, aba_grade_prof, aba_janelas_prof = st.tabs([
        "👥 Cadastro de professores",
        "📅 Grade de horários (Turno 1)",
        "🍽️ Almoço e Hora de Estudos"
    ])'''

if old_tabs in texto:
    texto = texto.replace(old_tabs, new_tabs, 1)
    print("tabs: 3 abas")
elif "aba_janelas_prof" in texto:
    print("tabs: ja existe aba janelas")
else:
    # tenta variante sem emoji de grade
    import re
    m = re.search(
        r"(\s*)(aba_cad_prof,\s*aba_grade_prof)\s*=\s*st\.tabs\(\[(.*?)\]\)",
        texto,
        re.DOTALL,
    )
    if not m:
        raise SystemExit("Nao achei st.tabs de professores")
    indent = m.group(1)
    new = (
        f"{indent}aba_cad_prof, aba_grade_prof, aba_janelas_prof = st.tabs([\n"
        f'{indent}    "👥 Cadastro de professores",\n'
        f'{indent}    "📅 Grade de horários (Turno 1)",\n'
        f'{indent}    "🍽️ Almoço e Hora de Estudos"\n'
        f"{indent}])"
    )
    texto = texto[: m.start()] + new + texto[m.end() :]
    print("tabs: substituido por regex")

# 2) Substituir corpo da aba grade + inserir aba janelas
inicio = texto.find("    with aba_grade_prof:")
if inicio == -1:
    raise SystemExit("Nao achei with aba_grade_prof")

fim = texto.find("    with aba_cad_prof:")
if fim == -1:
    fim = texto.find("# PÁGINA 👤 CADASTRAR ASSINATURAS")
    if fim == -1:
        raise SystemExit("Nao achei fim da aba grade")

novo = r'''
    with aba_grade_prof:
        st.subheader("Grade de horarios - Turno 1")
        st.caption("Padrao: disciplina em MAIUSCULAS | professor com iniciais maiusculas")

        try:
            carregar_grade_horaria.clear()
        except Exception:
            pass

        try:
            df_grade = carregar_grade_horaria("Turno 1", 2026)
        except Exception:
            df_grade = pd.DataFrame()

        if df_grade is None or df_grade.empty:
            st.warning("Grade ainda nao importada.")
        else:
            def _fmt_disc(v):
                return str(v or "").strip().upper()

            def _fmt_prof(v):
                s = str(v or "").strip()
                if not s:
                    return s
                partes = s.replace("_", " ").split()
                out = []
                for p in partes:
                    if len(p) <= 2 and p.endswith("."):
                        out.append(p[0].upper() + ".")
                    else:
                        out.append(p[:1].upper() + p[1:].lower())
                return " ".join(out)

            def _norm(v):
                return normalizar_texto(str(v or ""))

            df_g = df_grade.copy()
            df_g["disciplina"] = df_g["disciplina"].map(_fmt_disc)
            df_g["professor"] = df_g["professor"].map(_fmt_prof)
            df_g["aula"] = pd.to_numeric(df_g["aula"], errors="coerce").fillna(0).astype(int)

            professores = sorted({p for p in df_g["professor"] if p})
            dias_ord = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

            modo = st.radio(
                "Visualizacao",
                ["Resumo semanal (todos)", "Grade completa"],
                horizontal=True,
                key="modo_grade_horaria_v2",
            )

            if modo == "Resumo semanal (todos)":
                st.markdown("### Resumo de aulas por professor")
                linhas = []
                for prof in professores:
                    dfp = df_g[df_g["professor"].map(_norm) == _norm(prof)]
                    total = len(dfp)
                    row = {"Professor": prof, "Total semana": total}
                    for dia in dias_ord:
                        n = int((dfp["dia_semana"].astype(str).str.lower() == dia.lower()).sum())
                        row[dia] = n
                        row[f"Vago {dia}"] = 7 - n
                    linhas.append(row)
                df_res = pd.DataFrame(linhas).sort_values("Total semana", ascending=False)
                st.dataframe(df_res, use_container_width=True, hide_index=True)
                st.caption("Para montar almoco e Hora de Estudos, use a aba dedicada.")
            else:
                dia_filtro = st.selectbox(
                    "Dia",
                    ["Todos"] + dias_ord,
                    key="grade_completa_dia",
                )
                df_base = df_g.copy()
                if dia_filtro != "Todos":
                    df_base = df_base[
                        df_base["dia_semana"].astype(str).str.lower() == dia_filtro.lower()
                    ]

                def _tk(t):
                    s = str(t or "").upper().replace("º", "").replace("°", "")
                    s = s.replace(" ", "").replace("ANO", "").replace("-", "")
                    return s

                mapa_cols = [
                    ("6A", "6A"), ("6B", "6B"), ("7A", "7A"), ("7C", "7C"),
                    ("8A", "8A"), ("8B", "8B"), ("8C", "8C"),
                    ("9A", "9A"), ("9B", "9B"), ("9C", "9C"),
                    ("3ATEC", "3A-TEC"), ("3BTEC", "3B-TEC"),
                ]
                df_base["_tk"] = df_base["turma"].map(_tk)
                dias_show = dias_ord if dia_filtro == "Todos" else [dia_filtro]
                for dia in dias_show:
                    df_dia = df_base[df_base["dia_semana"].astype(str).str.lower() == dia.lower()]
                    if df_dia.empty:
                        continue
                    st.markdown(f"**{dia.upper()}**")
                    linhas = []
                    for aula in range(1, 8):
                        row = {"Aula": f"{aula}ª"}
                        df_aula = df_dia[df_dia["aula"] == aula]
                        for key, label in mapa_cols:
                            cel = df_aula[df_aula["_tk"] == key]
                            if cel.empty:
                                row[label] = ""
                            else:
                                r0 = cel.iloc[0]
                                row[label] = f"{r0['disciplina']} - {r0['professor']}"
                        linhas.append(row)
                    st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)

    with aba_janelas_prof:
        st.subheader("Almoco e Hora de Estudos")
        st.caption("Janelas VAGO de cada professor (1ª a 7ª) para encaixar almoco e Hora de Estudos")

        try:
            df_grade_j = carregar_grade_horaria("Turno 1", 2026)
        except Exception:
            df_grade_j = pd.DataFrame()

        if df_grade_j is None or df_grade_j.empty:
            st.warning("Grade ainda nao importada.")
        else:
            def _fmt_disc_j(v):
                return str(v or "").strip().upper()

            def _fmt_prof_j(v):
                s = str(v or "").strip()
                if not s:
                    return s
                partes = s.replace("_", " ").split()
                out = []
                for p in partes:
                    if len(p) <= 2 and p.endswith("."):
                        out.append(p[0].upper() + ".")
                    else:
                        out.append(p[:1].upper() + p[1:].lower())
                return " ".join(out)

            def _norm_j(v):
                return normalizar_texto(str(v or ""))

            df_j = df_grade_j.copy()
            df_j["disciplina"] = df_j["disciplina"].map(_fmt_disc_j)
            df_j["professor"] = df_j["professor"].map(_fmt_prof_j)
            df_j["aula"] = pd.to_numeric(df_j["aula"], errors="coerce").fillna(0).astype(int)

            professores_j = sorted({p for p in df_j["professor"] if p})
            dias_ord_j = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]

            col_a, col_b = st.columns(2)
            with col_a:
                prof_sel = st.selectbox("Professor(a)", professores_j, key="janela_prof_sel")
            with col_b:
                dia_foco = st.selectbox("Dia (opcional)", ["Todos"] + dias_ord_j, key="janela_dia_sel")

            dfp = df_j[df_j["professor"].map(_norm_j) == _norm_j(prof_sel)].copy()
            total_sem = len(dfp)

            c1, c2, c3 = st.columns(3)
            c1.metric("Aulas na semana", total_sem)
            c2.metric("Janelas VAGO na semana", max(35 - total_sem, 0))
            # 5 dias x 7 aulas = 35 slots

            dias_loop = dias_ord_j if dia_foco == "Todos" else [dia_foco]
            for dia in dias_loop:
                df_dia = dfp[dfp["dia_semana"].astype(str).str.lower() == dia.lower()]
                aulas_ocup = sorted(df_dia["aula"].unique().tolist()) if not df_dia.empty else []
                vagas = [a for a in range(1, 8) if a not in aulas_ocup]

                with st.expander(
                    f"{dia}  |  {len(aulas_ocup)} aula(s)  |  VAGO: {', '.join(str(v)+'ª' for v in vagas) if vagas else 'nenhum'}",
                    expanded=(dia == dias_loop[0]),
                ):
                    if aulas_ocup:
                        st.markdown("**Com aula**")
                        for _, r in df_dia.sort_values("aula").iterrows():
                            st.write(f"{int(r['aula'])}ª aula: {r['disciplina']} — {r['turma']}")
                    else:
                        st.write("Nenhuma aula neste dia.")

                    st.markdown(
                        "**VAGO:** "
                        + (", ".join(f"{v}ª" for v in vagas) if vagas else "NENHUM")
                    )
                    if vagas:
                        st.success(
                            "Sugestao de janelas para **almoco** / **Hora de Estudos**: "
                            + ", ".join(f"{v}ª" for v in vagas)
                        )

            st.markdown("---")
            st.markdown("### Visao geral de VAGO (todos os professores)")
            linhas_v = []
            for prof in professores_j:
                dfp2 = df_j[df_j["professor"].map(_norm_j) == _norm_j(prof)]
                row = {"Professor": prof, "Aulas semana": len(dfp2)}
                for dia in dias_ord_j:
                    n = int((dfp2["dia_semana"].astype(str).str.lower() == dia.lower()).sum())
                    row[f"Vago {dia}"] = 7 - n
                linhas_v.append(row)
            st.dataframe(
                pd.DataFrame(linhas_v).sort_values("Aulas semana", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

    with aba_cad_prof:
        st.caption("Cadastro e lista de professores")
'''

texto2 = texto[:inicio] + novo + texto[fim:]
path.write_text(texto2, encoding="utf-8")
print("ok: 3 abas + almoco/hora de estudos")
