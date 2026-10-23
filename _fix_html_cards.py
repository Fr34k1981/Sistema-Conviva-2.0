from pathlib import Path

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")

# Procura o bloco HTML dos cards de cafe/almoco e garante unsafe_allow_html
if "6º · 7º · 3º TEC" not in texto and "6º · 7º · 3º TEC" not in texto:
    # pode estar com encoding diferente
    pass

# Padrao comum: st.markdown(""" ... html ... """)  SEM unsafe_allow_html
# Troca o fechamento do markdown dos cards

import re

# Caso 1: markdown triplo com o div grid e fecha so com """)
padrao = re.compile(
    r'(st\.markdown\(\s*"""\s*\n?<div style="display:grid;grid-template-columns:1fr 1fr;[\s\S]*?</p>\s*\n?\s*"""\s*)\)',
    re.MULTILINE,
)

def repl(m):
    bloco = m.group(1)
    if "unsafe_allow_html" in bloco:
        return m.group(0)
    return bloco + ", unsafe_allow_html=True)"

texto2, n = padrao.subn(repl, texto, count=1)
print("regex_grid=", n)

if n == 0:
    # fallback: apos o trecho dos estudantes, se houver st.markdown sem flag
    idx = texto.find('display:grid;grid-template-columns:1fr 1fr')
    if idx == -1:
        raise SystemExit("Nao achei o HTML dos cards")
    # achar st.markdown antes
    inicio = texto.rfind("st.markdown(", 0, idx)
    if inicio == -1:
        raise SystemExit("Nao achei st.markdown dos cards")
    # achar fechamento """) proximo apos </p>
    fim_p = texto.find("</p>", idx)
    if fim_p == -1:
        raise SystemExit("Nao achei </p>")
    fim = texto.find('""")', fim_p)
    if fim == -1:
        fim = texto.find("''')", fim_p)
        if fim == -1:
            raise SystemExit("Nao achei fim do markdown")
        fecha = "''')"
    else:
        fecha = '""")'
    # ver o que vem depois de fecha
    depois = texto[fim:fim+40]
    if "unsafe_allow_html" in depois:
        print("ja tem unsafe_allow_html")
        texto2 = texto
    else:
        # """)  -> """, unsafe_allow_html=True)
        texto2 = texto[:fim] + '""", unsafe_allow_html=True)' + texto[fim+len(fecha):]
        print("ok: fallback unsafe_allow_html")
else:
    print("ok: regex unsafe_allow_html")

path.write_text(texto2, encoding="utf-8")
