from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Localiza e substitui o bloco "Tambem conta comunicados de atraso ja gravados"
inicio = texto.find("            # Tambem conta comunicados de atraso ja gravados")
if inicio == -1:
    inicio = texto.find("Tambem conta comunicados de atraso")
if inicio == -1:
    raise SystemExit("Nao achei bloco de contagem por comunicados")

# fim: ate ocorrencia_data["total_atrasos_aluno"]
fim = texto.find('ocorrencia_data["total_atrasos_aluno"] = total_atrasos_aluno', inicio)
if fim == -1:
    raise SystemExit("Nao achei total_atrasos_aluno")

# incluir a linha do total_atrasos
fim_linha = texto.find("\n", fim)
if fim_linha == -1:
    raise SystemExit("fim de linha")

novo = '''            # Contagem principal: comunicados de atraso do aluno (tabela comunicados)
            try:
                def _so_digitos(v):
                    return "".join(ch for ch in str(v or "") if ch.isdigit())

                ra_ref = _so_digitos(ra_aluno)
                df_com = carregar_comunicados()
                if df_com is not None and not df_com.empty and ra_ref:
                    df_ca = df_com.copy()
                    if "ra_aluno" in df_ca.columns:
                        df_ca["_ra"] = df_ca["ra_aluno"].map(_so_digitos)
                        df_ca = df_ca[df_ca["_ra"] == ra_ref]
                    if "tipo_comunicado" in df_ca.columns:
                        df_ca = df_ca[
                            df_ca["tipo_comunicado"].astype(str).str.lower().str.contains("atraso", na=False)
                            | df_ca.get("modelo", pd.Series(dtype=str)).astype(str).str.lower().str.contains("atraso", na=False)
                        ]
                    total_atrasos_aluno = max(total_atrasos_aluno, len(df_ca))
                    if not df_ca.empty and "data_comunicado" in df_ca.columns and pd.notna(data_ref):
                        datas_c = pd.to_datetime(df_ca["data_comunicado"], errors="coerce")
                        inicio_semana = data_ref - pd.Timedelta(days=int(data_ref.weekday()))
                        inicio_mes = data_ref.replace(day=1)
                        # recontagem limpa a partir dos comunicados (fonte oficial do atraso)
                        atrasos_semana_comunicado = int(
                            ((datas_c >= inicio_semana) & (datas_c <= data_ref)).sum()
                        )
                        atrasos_mes_comunicado = int(
                            ((datas_c >= inicio_mes) & (datas_c <= data_ref)).sum()
                        )
            except Exception as e:
                try:
                    logger.warning(f"Falha ao contar comunicados de atraso: {e}")
                except Exception:
                    pass

            ocorrencia_data["total_atrasos_aluno"] = total_atrasos_aluno
'''

texto2 = texto[:inicio] + novo + texto[fim_linha + 1:]
path.write_text(texto2, encoding="utf-8")
print("ok: contagem por comunicados de atraso")
