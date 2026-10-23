import ast
import os
import re
from pathlib import Path

ARQUIVO = Path("app.py")

print("=" * 80)
print("VARREDURA DO SISTEMA CONVIVA")
print("=" * 80)

# ------------------------------------------------------------
# 1. ARQUIVO
# ------------------------------------------------------------
print("\n[1] ARQUIVO")
print("Caminho:", ARQUIVO.resolve())
print("Tamanho:", ARQUIVO.stat().st_size, "bytes")
print("Modificado:", ARQUIVO.stat().st_mtime)

texto = ARQUIVO.read_text(encoding="utf-8", errors="replace")
linhas = texto.splitlines()

print("Linhas:", len(linhas))

# ------------------------------------------------------------
# 2. SINTAXE
# ------------------------------------------------------------
print("\n[2] SINTAXE PYTHON")

try:
    ast.parse(texto, filename=str(ARQUIVO))
    print("OK - AST válida")
except SyntaxError as e:
    print("ERRO DE SINTAXE")
    print("Linha:", e.lineno)
    print("Coluna:", e.offset)
    print("Mensagem:", e.msg)
    if e.lineno:
        inicio = max(0, e.lineno - 4)
        fim = min(len(linhas), e.lineno + 3)
        for i in range(inicio, fim):
            print(f"{i+1}: {linhas[i]!r}")

# ------------------------------------------------------------
# 3. PORTAS / CONEXÃO
# ------------------------------------------------------------
print("\n[3] POSTGRESQL / PORTAS")

for i, linha in enumerate(linhas, 1):
    if re.search(r"5436|5432|localhost|127\.0\.0\.1", linha, re.I):
        print(f"{i}: {linha}")

# ------------------------------------------------------------
# 4. SUPABASE
# ------------------------------------------------------------
print("\n[4] SUPABASE")

supabase = []
for i, linha in enumerate(linhas, 1):
    if re.search(r"supabase", linha, re.I):
        supabase.append((i, linha))

print("Quantidade de linhas contendo Supabase:", len(supabase))

for i, linha in supabase[:120]:
    print(f"{i}: {linha}")

if len(supabase) > 120:
    print("... restante omitido ...")

# ------------------------------------------------------------
# 5. TABELAS TUTORIA
# ------------------------------------------------------------
print("\n[5] TUTORIA / TABELAS")

for i, linha in enumerate(linhas, 1):
    if re.search(r"tutoria_responsaveis|tutoria_|tutoria", linha, re.I):
        if re.search(r"select|from|insert|update|delete|table|tutoria_responsaveis", linha, re.I):
            print(f"{i}: {linha}")

# ------------------------------------------------------------
# 6. POSSÍVEIS TABELAS SQL CITADAS
# ------------------------------------------------------------
print("\n[6] TABELAS SQL CITADAS NO APP")

tabelas = set()

padroes = [
    r'\bFROM\s+["`]?([A-Za-z_][A-Za-z0-9_]*)',
    r'\bJOIN\s+["`]?([A-Za-z_][A-Za-z0-9_]*)',
    r'\bINTO\s+["`]?([A-Za-z_][A-Za-z0-9_]*)',
    r'\bUPDATE\s+["`]?([A-Za-z_][A-Za-z0-9_]*)',
]

for padrao in padroes:
    for m in re.finditer(padrao, texto, re.I):
        tabelas.add(m.group(1))

for tabela in sorted(tabelas, key=str.lower):
    print(tabela)

# ------------------------------------------------------------
# 7. MOJIBAKE
# ------------------------------------------------------------
print("\n[7] CARACTERES CORROMPIDOS / MOJIBAKE")

mojibake = []

padrao_mojibake = re.compile(
    r"ðŸ|Ã.|Â.|â.|�"
)

for i, linha in enumerate(linhas, 1):
    if padrao_mojibake.search(linha):
        mojibake.append((i, linha))

print("Linhas suspeitas:", len(mojibake))

for i, linha in mojibake[:120]:
    print(f"{i}: {linha}")

if len(mojibake) > 120:
    print("... restante omitido ...")

# ------------------------------------------------------------
# 8. BACKSLASH + LINHA VAZIA
# ------------------------------------------------------------
print("\n[8] CONTINUAÇÕES QUEBRADAS (\\ + LINHA VAZIA)")

quebradas = []

for i in range(len(linhas) - 1):
    atual = linhas[i].rstrip()
    proxima = linhas[i + 1]

    if atual.endswith("\\") and not proxima.strip():
        quebradas.append((i + 1, atual))

print("Ocorrências:", len(quebradas))

for i, linha in quebradas[:100]:
    print(f"{i}: {linha}")

# ------------------------------------------------------------
# 9. LINHAS COM EMOJIS PROBLEMÁTICOS
# ------------------------------------------------------------
print("\n[9] EMOJIS SUSPEITOS")

for i, linha in enumerate(linhas, 1):
    if "ðŸ" in linha:
        print(f"{i}: {linha}")

# ------------------------------------------------------------
# 10. BACKUPS
# ------------------------------------------------------------
print("\n[10] BACKUPS DO APP.PY")

backups = sorted(
    Path(".").glob("app.py.backup*"),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

print("Quantidade:", len(backups))

for b in backups[:30]:
    print(b.name)

# ------------------------------------------------------------
# 11. ARQUIVOS DO PROJETO RELACIONADOS AO BANCO
# ------------------------------------------------------------
print("\n[11] ARQUIVOS DE BANCO / CONFIGURAÇÃO")

for p in sorted(Path(".").rglob("*")):
    if p.is_file() and (
        "database" in p.name.lower()
        or "postgres" in p.name.lower()
        or "supabase" in p.name.lower()
        or p.suffix.lower() in [".sql", ".env"]
    ):
        print(p)

print("\n" + "=" * 80)
print("FIM DA VARREDURA - NENHUM ARQUIVO FOI ALTERADO")
print("=" * 80)
