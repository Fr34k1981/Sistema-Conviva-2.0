from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

old = '''            # Data de referencia: ocorrencia selecionada OU data do comunicado
            data_ref = pd.to_datetime(
                ocorrencia_data.get("data", ""),
                errors="coerce",
                dayfirst=True
            )
            if pd.isna(data_ref):
                try:
                    data_ref = pd.to_datetime(data_comunicado)
                except Exception:
                    data_ref = pd.Timestamp.now().normalize()'''

new = '''            # Para ATRASO a data de referencia e SEMPRE a Data do comunicado.
            # Nao usar data de outra ocorrencia (ex.: cabular aula em maio),
            # senao os atrasos de setembro ficam zerados.
            try:
                data_ref = pd.to_datetime(data_comunicado)
            except Exception:
                data_ref = pd.to_datetime(
                    ocorrencia_data.get("data", ""),
                    errors="coerce",
                    dayfirst=True
                )
            if pd.isna(data_ref):
                data_ref = pd.Timestamp.now().normalize()'''

if old not in texto:
    raise SystemExit("Nao achei bloco data_ref")
texto = texto.replace(old, new, 1)
path.write_text(texto, encoding="utf-8")
print("ok: data_ref = data do comunicado")
