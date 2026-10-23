from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
texto = "".join(lines)

# Encontrar inicio: comentario cabecalho OU cols_h na aba janelas
ini = None
for key in [
    '            # cabecalho\n',
    '            cols_h = st.columns([0.8] + [1] * 5)\n',
    '            cols_h = st.columns([1.1] + [1] * 5)\n',
]:
    if key in texto:
        ini = texto.find(key)
        break
if ini is None:
    raise SystemExit("Nao achei cabecalho da grade janelas")

# Fim: botao salvar
keys_fim = [
    '            if st.button(\n                "💾 Salvar ALMOÇO / H.E."',
    '            if st.button("💾 Salvar ALMOÇO / H.E."',
]
fim = -1
for k in keys_fim:
    fim = texto.find(k, ini)
    if fim != -1:
        break
if fim == -1:
    # busca generica
    fim = texto.find("Salvar ALMOÇO", ini)
    if fim == -1:
        raise SystemExit("Nao achei Salvar ALMOCO")
    fim = texto.rfind("\n", ini, fim) + 1

novo = '''            # Horarios de referencia das aulas (Turno 1) + intervalos dos alunos
            HORARIO_AULA = {
                1: "07:00–07:50",
                2: "07:50–08:40",
                3: "09:00–09:50",
                4: "09:50–10:40",
                5: "10:40–11:30",
                6: "11:30–12:20",
                7: "12:20–13:10",
            }
            INTERVALOS_APOS = {
                2: ("☕ CAFÉ · 6º / 7º / 3º TEC", "08:40–09:00", "#dbeafe", "#1e3a8a"),
                3: ("☕ CAFÉ · 8º / 9º", "09:30–09:50", "#fef3c7", "#92400e"),
                4: ("🍽️ ALMOÇO · 6º / 7º / 3º TEC", "10:40–11:30", "#dbeafe", "#1e3a8a"),
                5: ("🍽️ ALMOÇO · 8º / 9º", "11:30–12:20", "#fef3c7", "#92400e"),
            }

            # cabecalho
            cols_h = st.columns([1.1] + [1] * 5)
            cols_h[0].markdown("**Aula / horário**")
            for i, dia in enumerate(dias_ord_j):
                cols_h[i + 1].markdown(f"**{dia[:3]}**")

            mudancas = []
            for aula in range(1, 8):
                cols = st.columns([1.1] + [1] * 5)
                hora = HORARIO_AULA.get(aula, "")
                cols[0].markdown(
                    f"**{aula}ª**<br><span style='font-size:0.75rem;color:#64748b'>{hora}</span>",
                    unsafe_allow_html=True,
                )
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

                if aula in INTERVALOS_APOS:
                    titulo_i, hora_i, bg_i, cor_i = INTERVALOS_APOS[aula]
                    st.markdown(
                        f"""
<div style="margin:0.25rem 0 0.55rem 0;padding:0.4rem 0.75rem;border-radius:8px;
background:{bg_i};border-left:4px solid {cor_i};font-size:0.82rem;color:{cor_i};font-weight:700;">
{titulo_i} &nbsp;·&nbsp; {hora_i}
</div>
""",
                        unsafe_allow_html=True,
                    )

'''

texto2 = texto[:ini] + novo + texto[fim:]
path.write_text(texto2, encoding="utf-8")
print("ok")
