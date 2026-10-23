from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# 1) Troca keys duplicadas para unicas
n = 0
def trocar(_m):
    global n
    n += 1
    return f'key="comunicado_data_atraso_{n}"'

texto2, q = re.subn(r'key\s*=\s*["\']comunicado_data_atraso["\']', trocar, texto)
print("keys_trocadas=%d" % q)

# 2) Se existir a key individual extra, mantém
print("individual=%d" % texto2.count("comunicado_data_atraso_individual"))

# 3) Remover date_input DUPLICADO no mesmo fluxo individual:
#    mantém só o PRIMEIRO data_atraso_comunicado = st.date_input(...)
padrao_bloco = re.compile(
    r'(\s*data_atraso_comunicado\s*=\s*st\.date_input\([\s\S]*?key\s*=\s*["\']comunicado_data_atraso_\d+["\']\s*\))',
    re.MULTILINE,
)
blocos = list(padrao_bloco.finditer(texto2))
print("blocos_date_input=%d" % len(blocos))

if len(blocos) >= 2:
    # remove do segundo em diante
    for b in reversed(blocos[1:]):
        texto2 = texto2[:b.start()] + texto2[b.end():]
    print("blocos_extras_removidos=%d" % (len(blocos) - 1))

path.write_text(texto2, encoding="utf-8")
print("ok")
