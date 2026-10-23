from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Remove TODOS os blocos data_atraso_comunicado = st.date_input(... key="comunicado_data_atraso")
padrao = re.compile(
    r"\n\s*data_atraso_comunicado\s*=\s*st\.date_input\(\s*"
    r"[^\)]*?key\s*=\s*[\"']comunicado_data_atraso[\"']\s*\)\s*",
    re.DOTALL,
)
texto2, n = padrao.subn("\n", texto)
print("removidos=%d" % n)

# Reinsere UMA vez, só no bloco individual de atraso, após justificativa
marcador = 'key="comunicado_justificativa_atraso"\n            )'
bloco = '''key="comunicado_justificativa_atraso"
            )

            data_atraso_comunicado = st.date_input(
                "Data do atraso",
                value=datetime.now().date(),
                format="DD/MM/YYYY",
                key="comunicado_data_atraso_individual"
            )'''

if marcador not in texto2:
    raise SystemExit("Nao achei o marcador da justificativa para reinseri a data.")

texto2 = texto2.replace(marcador, bloco, 1)

# Se o botão Salvar usa data_atraso_comunicado, ok.
# Garante que não restou key antiga duplicada
print("restante_key_antiga=%d" % texto2.count('key="comunicado_data_atraso"'))
print("nova_key=%d" % texto2.count("comunicado_data_atraso_individual"))

path.write_text(texto2, encoding="utf-8")
print("ok")
