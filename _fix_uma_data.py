from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

padrao = re.compile(
    r"\n[ \t]*data_atraso_comunicado\s*=\s*st\.date_input\("
    r"[\s\S]*?"
    r"key\s*=\s*[\"']comunicado_data_atraso[^\"']*[\"']\s*\)\s*",
    re.MULTILINE,
)
texto2, n = padrao.subn("\n", texto)
print("removidos=%d" % n)

marcador = 'key="comunicado_justificativa_atraso"\n            )'
if marcador not in texto2:
    raise SystemExit("Nao achei justificativa_atraso")

bloco = (
    'key="comunicado_justificativa_atraso"\n'
    "            )\n\n"
    "            data_atraso_comunicado = st.date_input(\n"
    '                "Data do atraso",\n'
    "                value=datetime.now().date(),\n"
    '                format="DD/MM/YYYY",\n'
    '                key="comunicado_data_atraso_unica"\n'
    "            )"
)

texto2 = texto2.replace(marcador, bloco, 1)

q = len(re.findall(r"data_atraso_comunicado\s*=\s*st\.date_input", texto2))
print("date_input_restantes=%d" % q)
if q != 1:
    raise SystemExit("Ainda nao ficou 1 campo. Pare.")

path.write_text(texto2, encoding="utf-8")
print("ok: apenas 1 Data do atraso")
