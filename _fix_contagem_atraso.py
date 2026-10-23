from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

old = '''            atrasos_semana_comunicado = 0
            atrasos_mes_comunicado = 0

            if (
                not ocorrencias_aluno.empty
                and "categoria" in ocorrencias_aluno.columns
            ):

                base_atrasos = ocorrencias_aluno.copy()

                categorias_atraso = (
                    base_atrasos["categoria"]
                    .fillna("")
                    .astype(str)
                    .str.upper()
                )

                base_atrasos = base_atrasos[
                    categorias_atraso.str.contains(
                        "ATRASO|ATRASADO|PONTUALIDADE",
                        regex=True,
                        na=False
                    )
                ].copy()

                if (
                    not base_atrasos.empty
                    and "data" in base_atrasos.columns
                ):

                    datas = pd.to_datetime(
                        base_atrasos["data"],
                        errors="coerce",
                        dayfirst=True
                    )

                    data_ref = pd.to_datetime(
                        ocorrencia_data.get("data", ""),
                        errors="coerce",
                        dayfirst=True
                    )

                    if pd.notna(data_ref):

                        inicio_semana = (
                            data_ref
                            - pd.Timedelta(
                                days=data_ref.weekday()
                            )
                        )

                        inicio_mes = data_ref.replace(day=1)

                        atrasos_semana_comunicado = int(
                            (
                                (datas >= inicio_semana)
                                & (datas <= data_ref)
                            ).sum()
                        )

                        atrasos_mes_comunicado = int(
                            (
                                (datas >= inicio_mes)
                                & (datas <= data_ref)
                            ).sum()
                        )'''

new = '''            atrasos_semana_comunicado = 0
            atrasos_mes_comunicado = 0
            total_atrasos_aluno = 0

            # Data de referencia: ocorrencia selecionada OU data do comunicado
            data_ref = pd.to_datetime(
                ocorrencia_data.get("data", ""),
                errors="coerce",
                dayfirst=True
            )
            if pd.isna(data_ref):
                try:
                    data_ref = pd.to_datetime(data_comunicado)
                except Exception:
                    data_ref = pd.Timestamp.now().normalize()

            if (
                not ocorrencias_aluno.empty
                and "categoria" in ocorrencias_aluno.columns
            ):
                base_atrasos = ocorrencias_aluno.copy()
                categorias_atraso = (
                    base_atrasos["categoria"]
                    .fillna("")
                    .astype(str)
                    .str.upper()
                )
                base_atrasos = base_atrasos[
                    categorias_atraso.str.contains(
                        "ATRASO|ATRASADO|PONTUALIDADE|CHEGAR",
                        regex=True,
                        na=False
                    )
                ].copy()

                total_atrasos_aluno = len(base_atrasos)

                if (
                    not base_atrasos.empty
                    and "data" in base_atrasos.columns
                    and pd.notna(data_ref)
                ):
                    datas = pd.to_datetime(
                        base_atrasos["data"],
                        errors="coerce",
                        dayfirst=True
                    )
                    inicio_semana = data_ref - pd.Timedelta(days=int(data_ref.weekday()))
                    inicio_mes = data_ref.replace(day=1)

                    atrasos_semana_comunicado = int(
                        ((datas >= inicio_semana) & (datas <= data_ref)).sum()
                    )
                    atrasos_mes_comunicado = int(
                        ((datas >= inicio_mes) & (datas <= data_ref)).sum()
                    )

            # Tambem conta comunicados de atraso ja gravados
            try:
                df_com = carregar_comunicados()
                if df_com is not None and not df_com.empty:
                    df_ca = df_com.copy()
                    if "ra_aluno" in df_ca.columns:
                        df_ca = df_ca[
                            df_ca["ra_aluno"].astype(str).str.replace(r"\\D", "", regex=True)
                            == str(ra_aluno).replace(" ", "")
                        ]
                    if "tipo_comunicado" in df_ca.columns:
                        df_ca = df_ca[
                            df_ca["tipo_comunicado"].astype(str).str.lower().str.contains("atraso", na=False)
                        ]
                    if not df_ca.empty and "data_comunicado" in df_ca.columns and pd.notna(data_ref):
                        datas_c = pd.to_datetime(df_ca["data_comunicado"], errors="coerce")
                        inicio_semana = data_ref - pd.Timedelta(days=int(data_ref.weekday()))
                        inicio_mes = data_ref.replace(day=1)
                        atrasos_semana_comunicado += int(
                            ((datas_c >= inicio_semana) & (datas_c <= data_ref)).sum()
                        )
                        atrasos_mes_comunicado += int(
                            ((datas_c >= inicio_mes) & (datas_c <= data_ref)).sum()
                        )
                        total_atrasos_aluno = max(total_atrasos_aluno, len(df_ca))
            except Exception:
                pass

            ocorrencia_data["total_atrasos_aluno"] = total_atrasos_aluno'''

if old not in texto:
    raise SystemExit("Nao achei bloco de contagem de atrasos")

texto = texto.replace(old, new, 1)

# PDF: ocorrencias anteriores = total de atrasos do aluno (nao total geral - 1)
old_pdf = '''        try:
            total_ocorrencias_int = int(total or 0)
            ocorrencias_anteriores = max(
                total_ocorrencias_int - 1,
                0
            )
        except Exception:
            ocorrencias_anteriores = 0'''

new_pdf = '''        try:
            total_atrasos_pdf = ocorrencia_data.get("total_atrasos_aluno")
            if total_atrasos_pdf is not None and str(total_atrasos_pdf).strip() != "":
                ocorrencias_anteriores = max(int(total_atrasos_pdf), 0)
            else:
                total_ocorrencias_int = int(total or 0)
                ocorrencias_anteriores = max(total_ocorrencias_int - 1, 0)
        except Exception:
            ocorrencias_anteriores = 0'''

if old_pdf not in texto:
    raise SystemExit("Nao achei calculo ocorrencias_anteriores no PDF")
texto = texto.replace(old_pdf, new_pdf, 1)

# Nao transformar 0 em traco quando houver contagem real passada como 0
# (mantem traco so se string vazia)

path.write_text(texto, encoding="utf-8")
print("ok: contagem de atrasos corrigida")
