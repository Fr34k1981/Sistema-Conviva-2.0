from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

inicio = texto.find("    with aba_janelas_prof:")
if inicio == -1:
    raise SystemExit("Nao achei with aba_janelas_prof")

fim = texto.find("    with aba_cad_prof:")
if fim == -1:
    raise SystemExit("Nao achei with aba_cad_prof")

novo = r'''
    with aba_janelas_prof:
        st.subheader("Grade de janelas · Almoço e H.E.")
        st.caption("Clique nas células VAGO e marque ALMOÇO ou H.E. · aulas com turma ficam bloqueadas")

        try:
            df_grade_j = carregar_grade_horaria("Turno 1", 2026)
        except Exception:
            df_grade_j = pd.DataFrame()

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

        def _carregar_janelas():
            try:
                df = _supabase_get_dataframe(
                    "grade_janelas?select=id,professor,dia_semana,aula,tipo,ano_letivo&ano_letivo=eq.2026",
                    "carregar grade janelas"
                )
                return df if df is not None else pd.DataFrame()
            except Exception:
                return pd.DataFrame()

        def _salvar_janela(professor, dia, aula, tipo):
            dados = {
                "professor": professor,
                "dia_semana": dia,
                "aula": int(aula),
                "tipo": tipo,
                "ano_letivo": 2026,
            }
            # remove se vazio
            if not tipo or tipo == "—":
                try:
                    _supabase_request(
                        "DELETE",
                        f"grade_janelas?professor=eq.{requests.utils.quote(professor)}&dia_semana=eq.{requests.utils.quote(dia)}&aula=eq.{int(aula)}&ano_letivo=eq.2026",
                    )
                    return True
                except Exception:
                    return False
            # upsert via delete + insert simples
            try:
                _supabase_request(
                    "DELETE",
                    f"grade_janelas?professor=eq.{requests.utils.quote(professor)}&dia_semana=eq.{requests.utils.quote(dia)}&aula=eq.{int(aula)}&ano_letivo=eq.2026",
                )
            except Exception:
                pass
            try:
                return bool(salvar_comunicado) and _supabase_request("POST", "grade_janelas", data=dados)
            except Exception:
                try:
                    r = _supabase_request("POST", "grade_janelas", data=[dados] if False else dados)
                    return True
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
                    return False

        if df_grade_j is None or df_grade_j.empty:
            st.warning("Grade de aulas ainda nao importada.")
        else:
            df_j = df_grade_j.copy()
            df_j["disciplina"] = df_j["disciplina"].map(_fmt_disc_j)
            df_j["professor"] = df_j["professor"].map(_fmt_prof_j)
            df_j["aula"] = pd.to_numeric(df_j["aula"], errors="coerce").fillna(0).astype(int)

            professores_j = sorted({p for p in df_j["professor"] if p})
            dias_ord_j = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
            opcoes_cel = ["—", "ALMOÇO", "H.E."]

            prof_sel = st.selectbox("Professor(a)", professores_j, key="janela_grade_prof")
            dfp = df_j[df_j["professor"].map(_norm_j) == _norm_j(prof_sel)].copy()
            df_jan = _carregar_janelas()
            if df_jan is not None and not df_jan.empty:
                df_jan = df_jan[df_jan["professor"].map(_norm_j) == _norm_j(prof_sel)].copy()
            else:
                df_jan = pd.DataFrame(columns=["dia_semana", "aula", "tipo"])

            def _tipo_salvo(dia, aula):
                if df_jan is None or df_jan.empty:
                    return "—"
                m = df_jan[
                    (df_jan["dia_semana"].astype(str).str.lower() == dia.lower())
                    & (pd.to_numeric(df_jan["aula"], errors="coerce") == aula)
                ]
                if m.empty:
                    return "—"
                return str(m.iloc[0].get("tipo", "—")).strip() or "—"

            st.markdown(f"**Grade de {prof_sel}** · Turno 1")
            st.caption("Células com turma = aula fixa · células livres = escolha ALMOÇO ou H.E.")

            # cabecalho
            cols_h = st.columns([0.8] + [1] * 5)
            cols_h[0].markdown("**Aula**")
            for i, dia in enumerate(dias_ord_j):
                cols_h[i + 1].markdown(f"**{dia[:3]}**")

            mudancas = []
            for aula in range(1, 8):
                cols = st.columns([0.8] + [1] * 5)
                cols[0].markdown(f"**{aula}ª**")
                for i, dia in enumerate(dias_ord_j):
                    df_cel = dfp[
                        (dfp["dia_semana"].astype(str).str.lower() == dia.lower())
                        & (dfp["aula"] == aula)
                    ]
                    with cols[i + 1]:
                        if not df_cel.empty:
                            r0 = df_cel.iloc[0]
                            st.text_input(
                                "aula",
                                value=f"{r0['disciplina']} | {r0['turma']}",
                                disabled=True,
                                key=f"fix_aula_{prof_sel}_{dia}_{aula}",
                                label_visibility="collapsed",
                            )
                        else:
                            atual = _tipo_salvo(dia, aula)
                            idx = opcoes_cel.index(atual) if atual in opcoes_cel else 0
                            novo_val = st.selectbox(
                                "janela",
                                opcoes_cel,
                                index=idx,
                                key=f"fix_janela_{prof_sel}_{dia}_{aula}",
                                label_visibility="collapsed",
                            )
                            mudancas.append((dia, aula, novo_val))

            if st.button("💾 Salvar ALMOÇO / H.E.", type="primary", key="btn_salvar_janelas_grade"):
                ok = 0
                falha = 0
                for dia, aula, tipo in mudancas:
                    # gravar via SQL direto se _supabase falhar
                    try:
                        import psycopg2
                        conn = psycopg2.connect(
                            host="127.0.0.1", port=5432, dbname="sistema_escolar",
                            user="escola_admin", password=""
                        )
                        cur = conn.cursor()
                        cur.execute(
                            "DELETE FROM grade_janelas WHERE professor=%s AND dia_semana=%s AND aula=%s AND ano_letivo=2026",
                            (prof_sel, dia, int(aula)),
                        )
                        if tipo and tipo != "—":
                            cur.execute(
                                "INSERT INTO grade_janelas (professor, dia_semana, aula, tipo, ano_letivo) VALUES (%s,%s,%s,%s,2026)",
                                (prof_sel, dia, int(aula), tipo),
                            )
                        conn.commit()
                        cur.close()
                        conn.close()
                        ok += 1
                    except Exception:
                        falha += 1
                if ok:
                    st.success(f"Salvo ({ok} célula(s)).")
                    st.rerun()
                if falha:
                    st.error(f"{falha} falha(s) ao salvar.")

            # legenda
            st.markdown("---")
            c1, c2, c3 = st.columns(3)
            total_aulas = len(dfp)
            n_almoco = sum(1 for d, a, t in mudancas if t == "ALMOÇO")
            n_he = sum(1 for d, a, t in mudancas if t == "H.E.")
            c1.metric("Aulas na semana", total_aulas)
            c2.metric("ALMOÇO marcados", n_almoco)
            c3.metric("H.E. marcados", n_he)

    with aba_cad_prof:
        st.caption("Cadastro e lista de professores")
'''

texto2 = texto[:inicio] + novo + texto[fim:]
path.write_text(texto2, encoding="utf-8")
print("ok: grade editavel ALMOCO / H.E.")
