from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Troca opcoes da celula para incluir P. PRESENCA
old_op = 'opcoes_cel = ["—", "ALMOÇO", "H.E."]'
new_op = 'opcoes_cel = ["—", "ALMOÇO", "H.E.", "P. PRESENÇA"]'
if old_op in texto:
    texto = texto.replace(old_op, new_op, 1)
    print("ok: opcao P. PRESENCA")
else:
    old_op2 = 'opcoes_cel = ["—", "ALMOCO", "H.E."]'
    if old_op2 in texto:
        texto = texto.replace(old_op2, new_op, 1)
        print("ok: opcao P. PRESENCA (alt)")
    else:
        print("AVISO: opcoes_cel nao encontrada")

# Inserir bloco de impressao no final da aba janelas, antes de with aba_cad_prof
marcador = "    with aba_cad_prof:"
if marcador not in texto:
    raise SystemExit("Nao achei with aba_cad_prof")

# so inserir se ainda nao existe
if "btn_imprimir_grade_janelas" in texto:
    print("impressao ja existe")
else:
    bloco_print = r'''
            st.markdown("---")
            st.markdown("### Impressao")
            st.caption("Gera pagina para imprimir ou salvar em PDF pelo navegador (Ctrl+P).")

            def _html_impressao_professor(prof, df_aulas, df_janelas_prof, dias_ord):
                # monta tabela 7 x 5
                def cel(dia, aula):
                    df_cel = df_aulas[
                        (df_aulas["dia_semana"].astype(str).str.lower() == dia.lower())
                        & (df_aulas["aula"] == aula)
                    ]
                    if not df_cel.empty:
                        r0 = df_cel.iloc[0]
                        return f"{r0['disciplina']}<br><small>{r0['turma']}</small>"
                    if df_janelas_prof is not None and not df_janelas_prof.empty:
                        m = df_janelas_prof[
                            (df_janelas_prof["dia_semana"].astype(str).str.lower() == dia.lower())
                            & (pd.to_numeric(df_janelas_prof["aula"], errors="coerce") == aula)
                        ]
                        if not m.empty:
                            return f"<b>{m.iloc[0].get('tipo','')}</b>"
                    return "—"

                rows = ""
                for aula in range(1, 8):
                    rows += f"<tr><th>{aula}ª</th>"
                    for dia in dias_ord:
                        rows += f"<td>{cel(dia, aula)}</td>"
                    rows += "</tr>"

                return f"""
<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Grade - {prof}</title>
<style>
body{{font-family:Arial,sans-serif;padding:16px;color:#111}}
h1{{font-size:18px;margin:0 0 8px 0}}
h2{{font-size:14px;margin:16px 0 6px 0;color:#333}}
table{{border-collapse:collapse;width:100%;font-size:11px}}
th,td{{border:1px solid #333;padding:6px;text-align:center;vertical-align:middle}}
th{{background:#e5e7eb}}
.legenda{{font-size:12px;margin-top:12px;line-height:1.5}}
.box{{display:inline-block;padding:8px 12px;border:1px solid #94a3b8;border-radius:6px;margin:4px 8px 4px 0}}
@media print{{button{{display:none}}}}
</style></head><body>
<h1>Grade do professor: {prof} · Turno 1</h1>
<p>Pedagogia da Presença só em janela livre de 1 aula (50 min). ALMOÇO e H.E. também só em VAGO.</p>
<table>
<thead><tr><th>Aula</th><th>Seg</th><th>Ter</th><th>Qua</th><th>Qui</th><th>Sex</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<h2>Intervalos dos estudantes</h2>
<div class="legenda">
  <div class="box"><b>6º · 7º · 3º TEC</b><br>Café 08:40–09:00<br>Almoço 10:40–11:30</div>
  <div class="box"><b>8º · 9º</b><br>Café 09:30–09:50<br>Almoço 11:30–12:20</div>
</div>
<p class="legenda">Gerado pelo Sistema Conviva 179</p>
</body></html>
"""

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                if st.button("🖨️ Imprimir grade deste professor", key="btn_imprimir_grade_janelas", use_container_width=True):
                    html = _html_impressao_professor(prof_sel, dfp, df_jan if 'df_jan' in dir() else pd.DataFrame(), dias_ord_j)
                    st.download_button(
                        "📥 Baixar HTML para impressão",
                        data=html.encode("utf-8"),
                        file_name=f"grade_{str(prof_sel).replace(' ','_')}.html",
                        mime="text/html",
                        key="dl_html_grade_prof",
                    )
                    st.components.v1.html(html, height=520, scrolling=True)
                    st.info("Use Ctrl+P na área acima ou abra o HTML baixado para imprimir/PDF.")
            with col_p2:
                if st.button("🖨️ Imprimir resumo de VAGO (todos)", key="btn_imprimir_resumo_vago", use_container_width=True):
                    linhas_html = []
                    for prof in professores_j:
                        dfp2 = df_j[df_j["professor"].map(_norm_j) == _norm_j(prof)]
                        total = len(dfp2)
                        cells = "".join(
                            f"<td>{7 - int((dfp2['dia_semana'].astype(str).str.lower()==d.lower()).sum())}</td>"
                            for d in dias_ord_j
                        )
                        linhas_html.append(f"<tr><td>{prof}</td><td>{total}</td>{cells}</tr>")
                    html_r = f"""
<!DOCTYPE html><html><head><meta charset="utf-8"><title>Resumo VAGO</title>
<style>body{{font-family:Arial;padding:16px}}table{{border-collapse:collapse;width:100%;font-size:12px}}
th,td{{border:1px solid #333;padding:5px;text-align:center}}th{{background:#e5e7eb}}</style></head>
<body><h1>Resumo de janelas VAGO · Turno 1</h1>
<table><thead><tr><th>Professor</th><th>Aulas</th><th>Vago Seg</th><th>Vago Ter</th><th>Vago Qua</th><th>Vago Qui</th><th>Vago Sex</th></tr></thead>
<tbody>{''.join(linhas_html)}</tbody></table>
<p>6º/7º/3º TEC — Café 08:40–09:00 · Almoço 10:40–11:30<br>
8º/9º — Café 09:30–09:50 · Almoço 11:30–12:20</p>
</body></html>"""
                    st.download_button(
                        "📥 Baixar resumo HTML",
                        data=html_r.encode("utf-8"),
                        file_name="resumo_vago_professores.html",
                        mime="text/html",
                        key="dl_html_resumo_vago",
                    )
                    st.components.v1.html(html_r, height=420, scrolling=True)

'''
    texto = texto.replace(marcador, bloco_print + "\n" + marcador, 1)
    print("ok: botoes de impressao")

path.write_text(texto, encoding="utf-8")
print("fim")
