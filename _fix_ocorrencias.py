from pathlib import Path
import re

path = Path(r"C:\SistemaConviva\app.py")
texto = path.read_text(encoding="utf-8")
original = texto

n = 0

# Caso 1: linha quebrada com str(ocorrencias_anteriores) sem rótulo
p1 = re.compile(
    r'(\[\s*["\']RA:["\']\s*,\s*ra\s*\+\s*["\']\s+\|\s+Turma:\s+["\']\s*\+\s*turma\s*\]\s*,\s*)'
    r'\[\s*str\(\s*ocorrencias_anteriores\s*\)\s*,\s*["\']?["\']?\s*\]',
    re.DOTALL,
)
texto2, q = p1.subn(
    r'\1["Ocorrências anteriores:", str(ocorrencias_anteriores)]',
    texto,
    count=1,
)
if q:
    texto = texto2
    n += q

# Caso 2: valor direto sem str()
if n == 0:
    p2 = re.compile(
        r'(\[\s*["\']RA:["\']\s*,\s*ra\s*\+\s*["\']\s+\|\s+Turma:\s+["\']\s*\+\s*turma\s*\]\s*,\s*)'
        r'\[\s*ocorrencias_anteriores\s*,\s*["\']?["\']?\s*\]',
        re.DOTALL,
    )
    texto2, q = p2.subn(
        r'\1["Ocorrências anteriores:", str(ocorrencias_anteriores)]',
        texto,
        count=1,
    )
    if q:
        texto = texto2
        n += q

# Caso 3: normaliza rótulo se já existir com texto diferente
if n == 0:
    p3 = re.compile(
        r'\[\s*["\']Ocorr[^"\']*["\']\s*,\s*str\(\s*ocorrencias_anteriores\s*\)\s*\]'
    )
    texto2, q = p3.subn(
        '["Ocorrências anteriores:", str(ocorrencias_anteriores)]',
        texto,
        count=1,
    )
    if q:
        texto = texto2
        n += q

print("ocorrencias_fix=%d" % n)

if texto == original:
    idx = texto.find("ocorrencias_anteriores")
    if idx == -1:
        raise SystemExit("Nao achei ocorrencias_anteriores no app.py")
    print("--- trecho atual ---")
    print(texto[max(0, idx - 300) : idx + 300])
    raise SystemExit("Nenhuma alteracao aplicada. Me envie o trecho acima.")

path.write_text(texto, encoding="utf-8")
print("Arquivo atualizado com sucesso.")
