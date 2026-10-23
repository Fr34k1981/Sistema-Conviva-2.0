from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

marcador = '            with st.expander("📋 Ver por dia da semana", expanded=False):'
if marcador not in texto:
    raise SystemExit("Nao achei expander Ver por dia")

# Insere ANTES do expander a grade visual completa
bloco = r'''
            st.markdown("### 🗓️ Grade completa (modelo planilha)")
            st.caption("Turno 1 · mesma estrutura da grade oficial · professor selecionado fica em destaque")

            ordem_turmas = ["6ºA", "6ºB", "7ºA", "7ºC", "8ºA", "8ºB", "8ºC", "9ºA", "9ºB", "9ºC", "3ºA-TEC", "3ºB-TEC"]
            # normaliza nomes de turma da base para bater com a ordem
            def _norm_turma(t):
                t = str(t or "").strip().upper().replace(" ", "")
                t = t.replace("º", "º").replace("°", "º")
                return t

            df_full = df_grade.copy()
            df_full["_turma_n"] = df_full["turma"].map(_norm_turma)
            df_full["_prof_n"] = df_full["professor"].astype(str).map(normalizar_texto)
            prof_n = normalizar_texto(prof_grade_sel)

            for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]:
                df_dia = df_full[df_full["dia_semana"].astype(str).str.strip().str.lower() == dia.lower()]
                if df_dia.empty:
                    continue
                st.markdown(f"**{dia.upper()}**")
                # monta matriz aula x turma
                linhas = []
                for aula in range(1, 8):
                    row = {"Aula": aula}
                    df_aula = df_dia[df_dia["aula"].astype(int) == aula]
                    for turma in ordem_turmas:
                        tn = _norm_turma(turma)
                        cel = df_aula[df_aula["_turma_n"] == tn]
                        if cel.empty:
                            # tenta match parcial
                            cel = df_aula[df_aula["_turma_n"].str.contains(tn.replace("º", ""), na=False)]
                        if cel.empty:
                            row[turma] = ""
                        else:
                            r0 = cel.iloc[0]
                            txt = f"{r0['disciplina']} - {r0['professor']}"
                            if prof_n and (prof_n in normalizar_texto(r0["professor"]) or normalizar_texto(r0["professor"]) in prof_n):
                                txt = f"★ {txt}"
                            row[turma] = txt
                    linhas.append(row)
                st.dataframe(pd.DataFrame(linhas), use_container_width=True, hide_index=True)

            with st.expander("📋 Ver por dia da semana", expanded=False):
'''

if "Grade completa (modelo planilha)" in texto:
    print("grade visual ja existe")
else:
    texto = texto.replace(marcador, bloco, 1)
    path.write_text(texto, encoding="utf-8")
    print("ok: grade visual inserida")
