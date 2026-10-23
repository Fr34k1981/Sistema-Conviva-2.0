from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

if "Grade de horários do professor" in texto or "grade_horaria_prof_sel" in texto:
    raise SystemExit("Secao de grade ja existe. Abortado.")

# Funcoes de carga (perto de carregar_professores)
marcador_fn = "@com_tratamento_erro\ndef atualizar_professor(id_prof: int, dados: dict) -> bool:"
if marcador_fn not in texto:
    # tenta sem decorator na mesma linha
    marcador_fn = "def atualizar_professor(id_prof: int, dados: dict) -> bool:"
if marcador_fn not in texto:
    raise SystemExit("Nao achei atualizar_professor")

funcoes = '''
@st.cache_data(ttl=600, show_spinner=False)
@com_tratamento_erro
def carregar_grade_horaria(turno: str = "Turno 1", ano_letivo: int = 2026) -> pd.DataFrame:
    """Carrega a grade oficial de aulas (disciplina + professor)."""
    try:
        turno_q = requests.utils.quote(str(turno), safe="")
        df = _supabase_get_dataframe(
            f"grade_horaria?select=id,turno,dia_semana,aula,turma,disciplina,professor,ano_letivo&turno=eq.{turno_q}&ano_letivo=eq.{int(ano_letivo)}&order=dia_semana.asc,aula.asc,turma.asc",
            "carregar grade horaria"
        )
        if df is None or df.empty:
            return pd.DataFrame()
        return df
    except Exception:
        return pd.DataFrame()


def _filtrar_grade_por_professor(df_grade: pd.DataFrame, nome_prof: str) -> pd.DataFrame:
    if df_grade is None or df_grade.empty or not nome_prof:
        return pd.DataFrame()
    chave = normalizar_texto(nome_prof)
    # aceita nome curto da grade (ELIANE) dentro do nome completo do cadastro
    def match(row_prof: str) -> bool:
        p = normalizar_texto(row_prof)
        if not p:
            return False
        return p in chave or chave in p or p.split()[0] in chave
    mask = df_grade["professor"].astype(str).apply(match)
    return df_grade[mask].copy()


'''

texto = texto.replace(marcador_fn, funcoes + marcador_fn, 1)

# UI no final da pagina Cadastrar Professores, antes de Cadastrar Assinaturas
marcador_ui = '''    else:
        st.info("📭 Nenhum professor cadastrado.")
        # ======================================================
# PÁGINA 👤 CADASTRAR ASSINATURAS (COMPLETA)
# ======================================================

elif menu == "👤 Cadastrar Assinaturas":'''

bloco_ui = '''    else:
        st.info("📭 Nenhum professor cadastrado.")

    # --------------------------------------------------
    # GRADE DE HORÁRIOS (Turno 1)
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("📅 Grade de horários do professor")
    st.caption("Quadro oficial de aulas · Turno 1 · Consulta por professor")

    try:
        df_grade = carregar_grade_horaria("Turno 1", 2026)
    except Exception:
        df_grade = pd.DataFrame()

    if df_grade is None or df_grade.empty:
        st.warning("⚠️ Grade ainda não importada. Importe o Turno 1 na base grade_horaria.")
    else:
        professores_grade = sorted(
            {str(p).strip() for p in df_grade["professor"].dropna().astype(str) if str(p).strip()}
        )
        nomes_cadastro = []
        if not df_professores.empty and "nome" in df_professores.columns:
            nomes_cadastro = sorted(
                df_professores["nome"].dropna().astype(str).str.strip().unique().tolist()
            )

        opcoes_prof = professores_grade[:]
        for n in nomes_cadastro:
            if n not in opcoes_prof:
                opcoes_prof.append(n)
        opcoes_prof = sorted(opcoes_prof)

        col_g1, col_g2 = st.columns([2, 1])
        with col_g1:
            prof_grade_sel = st.selectbox(
                "Professor(a)",
                opcoes_prof,
                key="grade_horaria_prof_sel",
            )
        with col_g2:
            dia_filtro = st.selectbox(
                "Dia",
                ["Todos", "Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
                key="grade_horaria_dia_sel",
            )

        df_prof = _filtrar_grade_por_professor(df_grade, prof_grade_sel)
        if dia_filtro != "Todos" and not df_prof.empty:
            df_prof = df_prof[
                df_prof["dia_semana"].astype(str).str.strip().str.lower()
                == dia_filtro.strip().lower()
            ]

        if df_prof.empty:
            st.info(f"Nenhuma aula encontrada para **{prof_grade_sel}** na grade.")
        else:
            ordem_dias = {"Segunda": 1, "Terça": 2, "Terca": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5}
            df_show = df_prof.copy()
            df_show["_ord"] = df_show["dia_semana"].map(lambda d: ordem_dias.get(str(d), 99))
            df_show = df_show.sort_values(["_ord", "aula", "turma"])
            tabela = df_show[["dia_semana", "aula", "turma", "disciplina", "professor"]].rename(
                columns={
                    "dia_semana": "Dia",
                    "aula": "Aula",
                    "turma": "Turma",
                    "disciplina": "Disciplina",
                    "professor": "Professor",
                }
            )
            st.success(f"**{len(tabela)}** aula(s) de **{prof_grade_sel}**")
            st.dataframe(tabela, use_container_width=True, hide_index=True)

            # Visao por dia (grade legivel)
            with st.expander("📋 Ver por dia da semana", expanded=False):
                for dia in ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]:
                    df_dia = df_show[df_show["dia_semana"].astype(str).str.lower() == dia.lower()]
                    if df_dia.empty:
                        continue
                    st.markdown(f"**{dia}**")
                    st.dataframe(
                        df_dia[["aula", "turma", "disciplina"]].rename(
                            columns={"aula": "Aula", "turma": "Turma", "disciplina": "Disciplina"}
                        ),
                        use_container_width=True,
                        hide_index=True,
                    )

    # ======================================================
# PÁGINA 👤 CADASTRAR ASSINATURAS (COMPLETA)
# ======================================================

elif menu == "👤 Cadastrar Assinaturas":'''

if marcador_ui not in texto:
    raise SystemExit("Nao achei o marcador final de Cadastrar Professores")

texto = texto.replace(marcador_ui, bloco_ui, 1)
path.write_text(texto, encoding="utf-8")
print("ok: grade em Cadastrar Professores")
