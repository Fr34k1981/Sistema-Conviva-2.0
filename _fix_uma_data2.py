from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

out = []
i = 0
removidos = 0
while i < len(lines):
    line = lines[i]
    if "data_atraso_comunicado = st.date_input" in line:
        # pula o bloco inteiro até fechar o )
        removidos += 1
        depth = 0
        while i < len(lines):
            l = lines[i]
            depth += l.count("(") - l.count(")")
            i += 1
            if depth <= 0:
                break
        # remove linhas em branco extras seguintes
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        continue
    out.append(line)
    i += 1

texto = "".join(out)

marcador = 'key="comunicado_justificativa_atraso"\n            )'
if marcador not in texto:
    raise SystemExit("Nao achei justificativa_atraso")

bloco = (
    'key="comunicado_justificativa_atraso"\n'
    "            )\n\n"
    "            data_atraso_comunicado = st.date_input(\n"
    '                "Data do atraso",\n'
    "                value=datetime.now().date(),\n"
    '                format="DD/MM/YYYY",\n'
    '                key="comunicado_data_atraso_unica"\n'
    "            )\n"
)

texto = texto.replace(marcador, bloco, 1)

q = texto.count("data_atraso_comunicado = st.date_input")
print("removidos=%d" % removidos)
print("date_input_restantes=%d" % q)
if q != 1:
    raise SystemExit("Ainda nao ficou 1 campo.")

path.write_text(texto, encoding="utf-8")
print("ok")
